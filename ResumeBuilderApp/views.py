from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from xhtml2pdf import pisa
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from io import BytesIO


def home(request):
    return render(request, 'pages/home.html')


def dashboard(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')
    return render(request, 'pages/Dashboard.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('inputEmail')
        password = request.POST.get('inputPassword')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or password is incorrect.')
            return render(request, 'pages/login.html')
    # GET request should render login page without any context data
    return render(request, 'pages/login.html')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            if user is not None:
              messages.success(request, 'Account was created for ' + user)
            else:
              messages.error(request, 'Account was not created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'pages/register.html', context)


def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def edit_user(request, user_id): # User editing
  user = User.objects.get(id=user_id)
  if request.method == 'POST':
    if request.POST.get("option","") == "User Info":
      form = UserEditForm(request.POST, instance=user)
      if form.is_valid():
          form.save()
    if request.POST.get("option","") == "Add Education":
      EduForm = EducationForm(request.POST)
      if EduForm.is_valid() and EduForm.cleaned_data.get("institution_name",""):
          name = EduForm.cleaned_data.get("institution_name","")
          degree = EduForm.cleaned_data.get("degree","")
          major = EduForm.cleaned_data.get("major","")
          start_date = datetime.strptime(request.POST.get("start_date",""), '%Y-%m-%d')
          end_date = datetime.strptime(request.POST.get("end_date",""), '%Y-%m-%d')

          Education(user=user, institution_name=name, degree=degree, major=major, 
                    start_date=start_date, end_date=end_date).save()
    if request.POST.get("option","") == "Add Skill":
      skillForm = SkillForm(request.POST)
      if skillForm.is_valid() and skillForm.cleaned_data.get("skill_name",""):
          skill = skillForm.save(commit=False)
          skill.user = request.user  # Assuming you're using user authentication
          skill.save()
    if request.POST.get("option","") == "Add Experience":
      jobForm = JobForm(request.POST)
      if jobForm.is_valid() and jobForm.cleaned_data.get("company_name",""):
          company_name = jobForm.cleaned_data.get("company_name","")
          role = jobForm.cleaned_data.get("role","")
          location = jobForm.cleaned_data.get("location","")
          description = jobForm.cleaned_data.get("description","")
          start_date = datetime.strptime(request.POST.get("start_date",""), '%Y-%m-%d')
          end_date = datetime.strptime(request.POST.get("end_date",""), '%Y-%m-%d')
          Job(user=user, company_name=company_name, role=role, location=location,
              description=description, start_date=start_date, end_date=end_date).save()
          
    return render(request, 'pages/Dashboard.html')  # Redirect to dashboard after editing
      
  else:
    form = UserEditForm(instance=user)
    return render(request, 'pages/edit_user.html', {'form1': form, 'form2':EducationForm(), 
                                                    'form3': SkillForm(), 'form4':JobForm()})

def editor(request):
    context = {}
    return render(request, 'pages/editor.html', context)

#function to save resume
def saveResume(request):
  if request.method == 'POST':
    content = request.POST.get('data', 'Hello World!')
    print(request.POST)
    #if we want to check resume contents for security reasons
    #check if user is logged in
    if not request.user.is_authenticated:
      return redirect('login')
    #retrieve user id from session and check if id is in session
    user_id = request.session.get('user_id')
    if not user_id:
      return redirect('login')
    #saves resume to database
    user = User.objects.get(id=user_id)
    #creates a pdf based of resume content
    resumeCount = Resume.objects.filter(user=user).count()
    resumePDF = BytesIO()
    pisa.CreatePDF(content, resumePDF)
    resume = Resume(name= "Resume" + str(resumeCount), user=user, resume_file=content)
    resume.save()
    if request.POST.get("chosen","") == "save":
        resumePDF.close()
        return render(request, 'pages/editor.html', {"currentContent": content})
    response = HttpResponse(resumePDF.getvalue(),content_type='application/pdf')
    response['Content'] = 'attachment; filename="Resume.pdf"'
    resumePDF.close()
    return response
  else:
    return redirect('editor')
