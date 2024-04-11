from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


#  create User model extending AbstractBaseUser and PermissionsMixin
class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=40, blank=True)
    last_name = models.CharField(_("last name"), max_length=40, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=40, blank=True, null=True)
    # more fields to add - TBD

    # fields below are admin fields from the auth.user class

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    # sets username field
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")


# more classes can be added below - TBD
# resume model 
class Resume(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.TextField(max_length=500000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


# TBD - this is for the quickResume view - need to decide if the resume models should merge
class quickResume(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(null=True, blank=True) #models.BinaryField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.company_name + " - " + self.role


class EducationChoices(models.TextChoices):
    HS = "High School"
    BS = "Bachelors of Science"
    BA = "Bachelors of Arts"
    MA = "Master of Arts"
    MS = "Master of Science"
    PHD = "Doctor of Philosophy"


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=150)
    degree = models.CharField(choices=EducationChoices.choices, max_length=100)
    major = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    objects = models.Manager()

    def __str__(self):
        return self.institution_name + " - " + self.degree + " - " + self.major


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=150)
    description = models.TextField()
    objects = models.Manager()

    def __str__(self):
        return self.skill_name

