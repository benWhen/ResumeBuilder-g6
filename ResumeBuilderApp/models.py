from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Languages(models.Model):
    language = models.CharField(max_length=100, unique=True)

class Interests(models.Model):
    interest = models.CharField(max_length=100, unique=True)
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and return a new user instance
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create and return a new superuser instance
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class MyUser(AbstractUser):
    username = models.CharField(max_length=64, blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
    password = models.CharField(max_length=128, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20,blank=True, null=True, unique=True)
    address = models.CharField(max_length=255)
    linkedin_url = models.URLField(max_length=200)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill) #Makes it so that skills can be added to database;therefore, usable for all
    languages = models.ManyToManyField(Languages)
    interests = models.ManyToManyField(Interests)
    groups = models.ManyToManyField('auth.Group',
                                    related_name='custom_user_set',
                                    blank=True,
                                    help_text='The groups this user '
                                              'belongs to. A user will '
                                              'get all permissions granted '
                                              'to each of their groups.')
    user_permissions = models.ManyToManyField('auth.Permission',
                                              related_name='custom_user_set',
                                              blank=True,
                                              help_text='Specific permissions for this user.')

    def __str__(self):
        return self.username
    """
    Checks if instance is being created (i.e. not updated)
    If instance is new, then hashes password.Otherwise 
    password is not hashed. In either instance, method calls 
    parent's save()
    """
    def save(self, *args, **kwargs):
        if self.pk is None:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    objects = MyUserManager()


class Education(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    degree_obtained = models.CharField(max_length=100)
    institution_attended = models.CharField(max_length=100)
    graduation_date = models.DateField()
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    relevant_coursework = models.TextField()

class WorkExperience(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    employer = models.CharField(max_length=100)
    duties = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

class Projects(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    description = models.TextField()

class CertificationsAndAwards(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()