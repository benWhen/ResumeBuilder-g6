from django.db import models

# Create your models here.


class Admin(models.Model):
    username = models.CharField(max_length=20, default="Admin")
    password = models.CharField(max_length=20, default="Password")
    email = models.EmailField(max_length=40, default="admin@uwm.edu")


class User(models.Model):
    username = models.CharField(max_length=20, default="Username")
    password = models.CharField(max_length=20, default="Password")
    first_name = models.CharField(max_length=20, default="First Name")
    last_name = models.CharField(max_length=20, default="Last Name")
    email = models.EmailField(max_length=40, default="email@uwm.edu")
    phone_number = models.IntegerField(max_length=10, default=4141234567)
    address = models.CharField(max_length=40, default="Address")


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many->one relationship : education->user
    name = models.CharField(max_length=20, default="UWM")
    degree = models.CharField(max_length=20, default="Bachelors")
    major = models.CharField(max_length=20, default="CS")
    start_year = models.IntegerField(max_length=4, default=2020)
    grad_year = models.IntegerField(max_length=4, default=2024)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many->one relationship : job->user
    role = models.CharField(max_length=20, default="Role")
    company = models.CharField(max_length=20, default="Company")
    location = models.CharField(max_length=20, default="Location")
    start_year = models.IntegerField(max_length=4, default=2024)
    end_year = models.IntegerField(max_length=4, default=2024)
    description = models.TextField(default="Description of Role and position responsibilities")


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many->one relationship : skill->user
    name = models.CharField(max_length=20, default="Skill")
    description = models.TextField(default="Description of Skill")


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many->one relationship : user->resume
    name = models.CharField(max_length=20, default="Resume Name")


class Template(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)  # many->one relationship : template->resume
    name = models.CharField(max_length=20, default="Name")
    description = models.TextField(default="Description of Template")


