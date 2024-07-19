from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import AdminUser, Course, Subject
from .models import Instructor, Student
from .forms import UserRegistrationForm, CourseForm


class SignupViewTests(TestCase):
    """
    Tests for the signup view.
    """
    def test_signup_get(self):
        """
        Test GET request to the signup view. It should return the signup form.
        """
        response = self.client.get(reverse('management_app:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')
        self.assertIsInstance(response.context['form'], UserRegistrationForm)

    def test_signup_post_valid_admin(self):
        """
        Test POST request with valid data for creating an Admin user.
        """
        data = {'username': 'testadminuser',
                'email': 'testemail@gmail.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
                'user_type': 'Admin'}
        response = self.client.post(reverse('management_app:signup'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('management_app:login'))
        self.assertTrue(User.objects.filter(username='testadminuser').exists())

    def test_signup_post_invalid(self):
        """
        Test POST request with invalid data where passwords do not match.
        """
        data = {'username': 'invaliduser',
                'email': 'test@gmail.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'password1': 'password123',
                'password2': 'password',
                'user_type': 'Admin'}
        response = self.client.post(reverse('management_app:signup'), data)
        
        # Ensure the response uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

        # Get the form from the response context
        form = response.context['form']
        # Check for form errors
        # Ensure the form has errors and check for specific form error
        self.assertTrue(form.errors)
        self.assertIn('__all__', form.errors)
        self.assertEqual(form.errors['__all__'], ['The two password fields must match.'])

    def test_signup_post_valid_instructor(self):
        """
        Test POST request with valid data for creating an Instructor user.
        """
        data = {'username': 'testinstructoruser',
                'email': 'test@gmail.com',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'password1': 'password',
                'password2': 'password',
                'user_type': 'Instructor'}
        response = self.client.post(reverse('management_app:signup'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('management_app:login'))
        self.assertTrue(User.objects.filter(username='testinstructoruser').exists())
    
    def test_signup_post_valid_student(self):
        """
        Test POST request with valid data for creating a Student user.
        """
        data = {'username': 'teststudentuser',
                'email': 'student@gmail.com',
                'first_name': 'Max',
                'last_name': 'Smith',
                'password1': 'password',
                'password2': 'password',
                'user_type': 'Student'}

        response = self.client.post(reverse('management_app:signup'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('management_app:login'))
        self.assertTrue(User.objects.filter(username='teststudentuser').exists())

