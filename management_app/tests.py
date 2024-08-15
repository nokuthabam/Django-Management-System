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


class SignInViewTests(TestCase):
    """
    Tests for the sign-in view.
    """
    def setUp(self):
        """
        Create an Admin user for testing.
        """
        # Sign up an admin user using sign up view
        data = {'username': 'testadminuser',
                'email': 'testemail@gmail.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
                'user_type': 'Admin'}
        self.client.post(reverse('management_app:signup'), data)

    def test_signin_get(self):
        """
        Test GET request to the sign-in view. 
        It should return the sign-in form.
        """
        response = self.client.get(reverse('management_app:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_signin_post_valid(self):
        """
        Test POST request with valid data for signing in.
        """
        data = {'username': 'testadminuser',
                'password': 'testpassword123'}

        response = self.client.post(reverse('management_app:login'), data)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, reverse('management_app:admin_home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_signin_post_invalid(self):
        """
        Test POST request with invalid data for signing in.
        """
        data = {'username': 'testadminuser',
                'password': 'invalidpassword'}

        response = self.client.post(reverse('management_app:login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


class CourseViewTests(TestCase):
    """
    Tests for the course view.
    """

    def setUp(self):
        """
        Create an Admin user for testing.
        """
        # Sign up an admin user using sign up view
        data = {'username': 'testadminuser',
                'email': 'testemail@gmail.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'password1': 'testpassword123',
                'password2': 'testpassword123',
                'user_type': 'Admin'}
        self.client.post(reverse('management_app:signup'), data)

    def test_course_get(self):
        """
        Test GET request to the course view. 
        It should return the course form.
        """
        self.client.login(username='testadminuser', password='testpassword123')
        response = self.client.get(reverse('management_app:course_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/course_templates/course_list.html')

    def test_course_create_valid(self):
        """
        Test POST request with valid data for creating a course.
        """
        self.client.login(username='testadminuser', password='testpassword123')
        data = {'name': 'Test Course',
                'description': 'Test Description'}
        response = self.client.post(reverse('management_app:course_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('management_app:course_list'))
        self.assertTrue(Course.objects.filter(name='Test Course').exists())

    def test_course_create_invalid(self):
        """
        Test POST request with invalid data for creating a course.
        """
        self.client.login(username='testadminuser', password='testpassword123')
        data = {'description': 'Test Description'}
        response = self.client.post(reverse('management_app:course_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/course_templates/course_form.html')
    
    def test_course_post_invalid_duplicate(self):
        """
        Test POST request with duplicate course.
        """
        self.client.login(username='testadminuser', password='testpassword123')
        Course.objects.create(name='Test Course', description='This is a test course.')
        data = {'course_name': 'Test Course',
                'course_description': 'This is a test course.'}
        response = self.client.post(reverse('management_app:course_create'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'management_app/course_templates/course_form.html')
        # Check if 'form' is in the context
        self.assertIn('form', response.context)

        # If form is present, check for errors
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['This field is required.'])

    def test_edit_course(self):
        """
        Test POST request with valid data for editing a course.
        """
        self.client.login(username='testadminuser', password='testpassword123')
        course = Course.objects.create(name='Test Course', description='This is a test course.')
        data = {'name': 'Edited Course',
                'description': 'Edited Description'}
        response = self.client.post(reverse('management_app:course_update', args=[course.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('management_app:course_list'))
        self.assertTrue(Course.objects.filter(name='Edited Course').exists())

    def test_delete_course(self):
        """
        Test POST request for deleting a course.
        """
        self.client.login(username='testadminuser', password='testpassword123')
        course = Course.objects.create(name='Test Course', description='This is a test course.')
        response = self.client.post(reverse('management_app:course_delete', args=[course.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('management_app:course_list'))
        self.assertFalse(Course.objects.filter(name='Test Course').exists())