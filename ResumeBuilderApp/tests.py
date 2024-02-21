from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Skill, Languages, Interests, MyUser, Education, WorkExperience, Projects, CertificationsAndAwards
from datetime import date

class TestMyUser(TestCase):
  def setUp(self):
    self.user = MyUser.objects.create_user(username='testuser',  
                                           email='email@example.com', 
                                           password='testpassword',
                                           first_name='test',
                                           last_name='name',
      )

  def test_user_creation(self):
    self.assertEqual(MyUser.objects.count(), 1)


# Create your tests here.
