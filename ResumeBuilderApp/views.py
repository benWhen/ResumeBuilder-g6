from django.shortcuts import render, redirect
from django.template import Template, Context
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from xhtml2pdf import pisa
from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
import json
from django.http import JsonResponse, HttpResponse
from django.core.files.base import ContentFile


def home(request):
    return render(request, 'pages/home.html')


def dashboard(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
    else:
        return redirect('login')
    resumes = Resume.objects.filter(user=user)
    resume_templates = get_template_library(request)
    return render(request, 'pages/Dashboard.html', {'resumes': resumes, 'resume_templates': resume_templates})


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
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        return render(request, 'pages/Dashboard.html' , {'resumes': Resume.objects.filter(user=user)})
        # Redirect to dashboard after editin
    else:
      return render(request, 'pages/edit_user.html', {'form1': UserEditForm(instance=user), 'form2':EducationForm(), 'form3':SkillForm(),'form4':JobForm()})


def add_Education(request):
    if not request.user.is_authenticated:
        return redirect('login')
      #retrieve user id from session and check if id is in session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
      #saves resume to database
    user = User.objects.get(id=user_id)
    EduForm = EducationForm(request.POST)
    if EduForm.is_valid() and EduForm.cleaned_data.get("institution_name",""):
        name = EduForm.cleaned_data.get("institution_name","")
        degree = EduForm.cleaned_data.get("degree","")
        major = EduForm.cleaned_data.get("major","")
        start_date = datetime.strptime(request.POST.get("start_date",""), '%Y-%m-%d')
        end_date = datetime.strptime(request.POST.get("end_date",""), '%Y-%m-%d')
        Education(user=user, institution_name=name, degree=degree, major=major,
                      start_date=start_date, end_date=end_date).save()
    return render(request, 'pages/edit_user.html', {'form1': UserEditForm(instance=user), 'form2':EducationForm(), 'form3':SkillForm(),'form4':JobForm()})

def add_Skill(request):
    if not request.user.is_authenticated:
        return redirect('login')
      #retrieve user id from session and check if id is in session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
      #saves resume to database
    user = User.objects.get(id=user_id)
    skillForm = SkillForm(request.POST)
    if skillForm.is_valid() and skillForm.cleaned_data.get("skill_name",""):
        skill = skillForm.save(commit=False)
        skill.user = user  # Assuming you're using user authentication
        skill.save()
        return render(request, 'pages/edit_user.html', {'form1': UserEditForm(instance=user), 'form2':EducationForm(), 'form3':SkillForm(),'form4':JobForm()})


def add_Job(request):
    if not request.user.is_authenticated:
        return redirect('login')
      #retrieve user id from session and check if id is in session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
      #saves resume to database
    user = User.objects.get(id=user_id)
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
    return render(request, 'pages/edit_user.html', {'form1': UserEditForm(instance=user), 'form2':EducationForm(), 'form3':SkillForm(),'form4':JobForm()})


def editor(request):
    context = {}
    return render(request, 'pages/editor.html', context)

  #function to save resume
def saveResume(request):
    if request.method == 'POST':
      content = request.POST.get('data', 'Hello World!')
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

def loadResume(request):
    print("loadResume")
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        #retrieve user id from session and check if id is in session
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('login')
        resumeName = request.POST.get('resumeName')
        if resumeName == "":
            resumes = Resume.objects.filter(user=request.user)
            return render(request, 'pages/dashboard.html', {"resumes": resumes})
        resume = Resume.objects.get(name=resumeName, user=request.user)
        return render(request, 'pages/editor.html', {"currentContent": resume.resume_file})
    else:
        resumes = Resume.objects.filter(user=request.user)
        return render(request, 'pages/dashboard.html', {"resumes": resumes})

def quickResume(request, user_id):
    data = User.objects.get(id=user_id)
    skills = Skill.objects.all()
    buffer=BytesIO()
    pdf=canvas.Canvas(buffer)
    # only adding skills for now - will add more later, and also font sizing and families
    x = 100; y =700
    for skill in skills:
        pdf.drawString(x, y, f"{skill.skill_name} - {skill.description}")
        x+=100; y+=100
    pdf.save()
    pdf_content=buffer.getvalue()
    buffer.close()

    resumeCount = quickResume.objects.filter(user=user_id).count()
    pdf_resume, created = quickResume.objects.get_or_create(name="Resume " + str(resumeCount), user_id=user_id)
    pdf_resume.pdf_file.save(f"Resume {resumeCount}.pdf", ContentFile(pdf_content), save=True) #pdf_resume.pdf_file = pdf_content #
    pdf_resume.save()

    response = HttpResponse(pdf_content,content_type='application/pdf')
    response['Content'] = 'attachment; filename="Resume.pdf"'
    return response


def get_template_library(request):
    jsonfile = open('ResumeBuilderApp/static/data/resume_templates.json', 'r')
    resume_templates = json.load(jsonfile)
    jsonfile.close()
    return resume_templates


def get_template(request, template_name):
    templates = get_template_library(request)
    for template in templates:
        if template['name'] == template_name:
            return template
    return None


def generate_resume(request, resume_template):
    # get user data
    user = request.user
    education = Education.objects.filter(user=user)
    skills = Skill.objects.filter(user=user)
    jobs = Job.objects.filter(user=user)
    user_data = {
        'user': user,
        'education': education,
        'skills': skills,
        'jobs': jobs
    }
    # reload templates to pull data from
    resume_template_full = get_template(request, resume_template)
    template_content = resume_template_full.get('content')
    # render the template with Django
    django_template = Template(template_content)
    rendered_template = django_template.render(Context(user_data))
    pdf_content = convert_to_pdf(rendered_template)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    response.write(pdf_content)
    return response


def convert_to_pdf(template_content):
    # PDF file buffer
    result_file = BytesIO()
    # PDF to HTML conversion
    pisa.CreatePDF(template_content.encode('utf-8'), dest=result_file)
    pdf_content = result_file.getvalue()
    # Close buffer
    result_file.close()
    return pdf_content

