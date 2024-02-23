from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Skill, Languages, Interests, MyUser, Education, WorkExperience, Projects, CertificationsAndAwards
from datetime import date
from django.contrib.auth.hashers import check_password
class TestMyUser(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(name='Programming')
        self.language = Languages.objects.create(language='Python')
        self.interest = Interests.objects.create(interest='Reading')

    def test_create_user(self):
        user = MyUser.objects.create_user(username='testuser',
                                                    first_name='John',
                                                    last_name='Doe',
                                                    email='test@example.com',
                                                    password='testpassword',
                                                    phone_number='1234567890',
                                                    address='123 Test St',
                                                    linkedin_url='http://linkedin.com/testuser',
                                                    bio='Test bio')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(check_password('testpassword', user.password))
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.address, '123 Test St')
        self.assertEqual(user.linkedin_url, 'http://linkedin.com/testuser')
        self.assertEqual(user.bio, 'Test bio')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        # Test creating a superuser
        User = get_user_model()
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )

        self.assertEqual(superuser.username, 'admin')
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(check_password('adminpassword', superuser.password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_create_education(self):
        user = MyUser.objects.create_user(username='testuser',
                                          email='test@example.com',
                                          password='testpassword')
        education = Education.objects.create(user=user,
                                             degree_obtained='Bachelor of Science',
                                             institution_attended='University of Test',
                                             graduation_date=date.today(),
                                             gpa=3.5,
                                             relevant_coursework='Computer Science, Mathematics')
        self.assertEqual(education.user, user)
        self.assertEqual(education.degree_obtained, 'Bachelor of Science')
        self.assertEqual(education.institution_attended, 'University of Test')
        self.assertEqual(education.graduation_date, date.today())
        self.assertEqual(education.gpa, 3.5)
        self.assertEqual(education.relevant_coursework, 'Computer Science, Mathematics')

    def test_create_work_experience(self):
        user = MyUser.objects.create_user(username='testuser',
                                          email='test@example.com',
                                          password='testpassword')
        work_experience = WorkExperience.objects.create(user=user,
                                                        title='Software Engineer',
                                                        employer='Tech Company',
                                                        duties='Developing software applications',
                                                        start_date=date(2020, 1, 1),
                                                        end_date=date(2021, 1, 1))
        self.assertEqual(work_experience.user, user)
        self.assertEqual(work_experience.title, 'Software Engineer')
        self.assertEqual(work_experience.employer, 'Tech Company')
        self.assertEqual(work_experience.duties, 'Developing software applications')
        self.assertEqual(work_experience.start_date, date(2020, 1, 1))
        self.assertEqual(work_experience.end_date, date(2021, 1, 1))

    def test_create_user_with_existing_email(self):
        MyUser.objects.create_user(username='testuser1',
                                   email='test@example.com',
                                   password='testpassword3')
        with self.assertRaises(ValidationError):
            MyUser.objects.create_user(username='testuser2',
                                       email='test@example.com',
                                       password='testpassword2')

    def test_create_user_with_existing_username(self):
        MyUser.objects.create_user(username='testuser1',
                                   email='test@example.com',
                                   password='testpassword3')
        with self.assertRaises(ValidationError):
            MyUser.objects.create_user(username='testuser1',
                                       email='test2@example.com',
                                       password='testpassword2')

    def test_create_user_with_invalid_email(self):
        with self.assertRaises(ValidationError):
            MyUser.objects.create_user(username='testuser2',
                                       email='invalidemail',
                                       password='testpassword2')

    def test_create_user_without_password(self):
        with self.assertRaises(ValueError):
            MyUser.objects.create_user(username='testuser2',
                                       email='test2@example.com')

    def test_create_user_with_empty_username(self):
        with self.assertRaises(ValidationError) as context:
            MyUser.objects.create_user(username='',
                                       email='test4@example.com',
                                       password='testpassword4')
        self.assertIn('username', context.exception.message_dict)
        self.assertIn('This field cannot be blank.', context.exception.message_dict['username'])

    def test_create_user_with_empty_email(self):
        with self.assertRaises(ValidationError) as context:
            MyUser.objects.create_user(username='testuser',
                                       email='',
                                       password='testpassword4')
        self.assertIn('email', context.exception.message_dict)
        self.assertIn('This field cannot be blank.', context.exception.message_dict['email'])

    def test_create_user_with_short_password(self):
        with self.assertRaises(ValidationError):
            MyUser.objects.create_user(username='testuser5',
                                       email='test5@example.com',
                                       password='test')

    def test_create_user_with_invalid_phone_number(self):
        with self.assertRaises(ValueError):
            MyUser.objects.create_user(username='testuser',
                                       email='test@example.com',
                                       password='testpassword',
                                       phone_number='123')

class TestModels(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            username='testuser',
            first_name='John',
            last_name='Doe',
            email='test@example.com',
            password='testpassword',
            phone_number='1234567890',
            address='123 Test St',
            linkedin_url='http://linkedin.com/testuser',
            bio='Test bio'
        )

        self.skill = Skill.objects.create(name='Programming')
        self.language = Languages.objects.create(language='Python')
        self.interest = Interests.objects.create(interest='Reading')

        self.education = Education.objects.create(
            user=self.user,
            degree_obtained='Bachelor of Science',
            institution_attended='University of Test',
            graduation_date=date(2020, 5, 15),
            gpa=3.5,
            relevant_coursework='Computer Science'
        )

        self.work_experience = WorkExperience.objects.create(
            user=self.user,
            title='Software Engineer',
            employer='Test Company',
            duties='Developed web applications',
            start_date=date(2020, 6, 1),
            end_date=date(2021, 6, 1)
        )

        self.project = Projects.objects.create(
            user=self.user,
            project_name='Project X',
            description='Developed a web application for project management'
        )

        self.certification = CertificationsAndAwards.objects.create(
            user=self.user,
            title='Certification X',
            description='Received Certification X for completion of course'
        )
        self.user.skills.add(self.skill)
        self.user.languages.add(self.language)
        self.user.interests.add(self.interest)


    def test_user_skills(self):
        self.assertIn(self.skill, self.user.skills.all())

    def test_user_languages(self):
        self.assertIn(self.language, self.user.languages.all())

    def test_user_interests(self):
        self.assertIn(self.interest, self.user.interests.all())

    def test_skill_creation(self):
        self.assertEqual(self.skill.name, 'Programming')

    def test_language_creation(self):
        self.assertEqual(self.language.language, 'Python')

    def test_interest_creation(self):
        self.assertEqual(self.interest.interest, 'Reading')

    def test_education_creation(self):
        self.assertEqual(self.education.user, self.user)
        self.assertEqual(self.education.degree_obtained, 'Bachelor of Science')

    def test_work_experience_creation(self):
        self.assertEqual(self.work_experience.user, self.user)
        self.assertEqual(self.work_experience.title, 'Software Engineer')

    def test_project_creation(self):
        self.assertEqual(self.project.user, self.user)
        self.assertEqual(self.project.project_name, 'Project X')

    def test_certification_creation(self):
        self.assertEqual(self.certification.user, self.user)
        self.assertEqual(self.certification.title, 'Certification X')




# Create your tests here.
