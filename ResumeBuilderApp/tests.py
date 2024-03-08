from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testPassword!123')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('login') + '?next=%2Fdashboard%2F')  # Check if the user is redirected to the login page

        self.client.login(username='testuser', password='testPassword!123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
    def test_user_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/login.html')

    def test_login_valid_data(self):
        login_data = {'username': 'testuser', 'password': 'testPassword!123'}
        response = self.client.post(reverse('login'), login_data)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_password(self):
        login_data = {'username': 'testuser', 'password': 'invalidpassword'}
        response = self.client.post(reverse('login'), login_data)
        self.assertContains(response, 'Username or password is incorrect.')

    def test_login_invalid_user(self):
        login_data = {'username': 'invaliduser', 'password': 'testPassword!123'}
        response = self.client.post(reverse('login'), login_data)
        self.assertContains(response, 'Username or password is incorrect.')
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username='invaliduser')

    def test_empty_login_credentials(self):
        login_data = {'username': '', 'password': ''}
        response = self.client.post(reverse('login'), login_data)
        self.assertContains(response, 'Username or password is incorrect.')

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/register.html')

    def test_register_valid_data(self):
        register_data = {'username': 'newuser', 'password1': 'SecurePassword!123', 'password2': 'SecurePassword!123'}
        response = self.client.post(reverse('register'), register_data)
        self.assertRedirects(response, reverse('login'))
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists, "User should be created with valid data")

    def test_max_length_username(self):
        long_username = 'a' * 151
        register_data = {'username': long_username, 'password1': 'ValidPassword!123', 'password2': 'ValidPassword!123'}
        response = self.client.post(reverse('register'), register_data, follow=True)
        self.assertContains(response, 'Ensure this value has at most 150 characters (it has 151).')
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=long_username)

    def test_special_chars_in_username(self):
        username = 'user!@#$'
        register_data = {'username': username, 'password1': 'ValidPassword!123', 'password2': 'ValidPassword!123'}
        response = self.client.post(reverse('register'), register_data)
        self.assertContains(response, 'Username can only contain letters, numbers, and underscores')
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username=username)

    def test_register_invalid_mismatching_password(self):
        register_data = {'username': 'newuser1', 'password1': 'SecurePassword!123', 'password2': 'SecurePassword'}
        response = self.client.post(reverse('register'), register_data)
        self.assertContains(response, 'The two password fields didn’t match.')
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username='newuser1')

    def test_logout(self):
        self.client.login(username='testuser', password='testPassword!123')
        self.assertTrue('_auth_user_id' in self.client.session)
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertFalse('_auth_user_id' in self.client.session)

