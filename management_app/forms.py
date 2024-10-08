# Import forms, models and users
from django import forms
from .models import Course, Subject, Student
from .models import AdminUser, Instructor, Grade
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# Create a form for registering a user
class UserRegistrationForm(forms.ModelForm):
    """
    Form for registering a user depending on the user type.
    Attributes:
        username (str): The user's username.
        email (str): The user's email address.
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        password (str): The user's password.

    Methods:
        clean_username: Ensure that the username is unique.
        save: Save the user object to the database.
    """
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    # user type
    user_type = forms.ChoiceField(choices=[
                ('Admin', 'Admin'),
                ('Instructor', 'Instructor'),
                ('Student', 'Student')
                ])

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2']

    def clean_username(self):
        """
        Ensure that the username is unique.
        """
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')
        return username
    
    def clean(self):
        """
        Ensure that the passwords match.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('The two password fields must match.')
        return cleaned_data
    
    def save(self, user_type):
        """
        Save the user object to the database.
        """
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            password=self.cleaned_data['password1']
        )
        if user_type == 'Admin':
            AdminUser.objects.create(user=user)
        elif user_type == 'Instructor':
            #Set default course and subject
            Instructor.objects.create(user=user, course_id=None, subject_id=None)
        else:
            # get the course
            # Set default course and subjects
            student = Student.objects.create(user=user, course_id=None)
            student.subjects.set([])
        return user
    

class CourseForm(forms.ModelForm):
    """
    Form for managing a course.
    Attributes:
        name (str): The course name.
        description (str): The course description.
    """
    name = forms.CharField(max_length=100)
    #description = forms.CharField(max_length=500)
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 7, 'cols': 60}),
        max_length=500)
    class Meta:
        model = Course
        fields = ['name', 'description']

    def clean_name(self):
        """
        Ensure that the course name is unique.
        """
        name = self.cleaned_data.get('name')
        if Course.objects.filter(name=name).exists():
            raise ValidationError('Course with this name already exists.')
        return name


class SubjectForm(forms.ModelForm):
    """
    Form for managing a subject.
    Attributes:
        name (str): The subject name.
        course (Course): The course to which the subject belongs.
    """
    name = forms.CharField(max_length=100)
    course_id = forms.ModelChoiceField(queryset=Course.objects.all())

    class Meta:
        model = Subject
        fields = ['name', 'course_id']


class StudentForm(forms.ModelForm):
    """
    Form for managing a student.
    Attributes:
        user (User): The user object associated with the student.
        course (Course): The course to which the student belongs.
        subjects (list of Subject): The subjects the student is taking.
    """
    user = forms.ModelChoiceField(queryset=User.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    subjects = forms.ModelMultipleChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = Student
        fields = ['user', 'course', 'subjects']


class InstructorForm(forms.ModelForm):
    """
    Form for managing an instructor.
    Attributes:
        user (User): The user object associated with the instructor.
        course (Course): The course to which the instructor belongs.
        subject (Subject): The subject the instructor teaches.
    """
    user = forms.ModelChoiceField(queryset=User.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = Instructor
        fields = ['user', 'course', 'subject']

