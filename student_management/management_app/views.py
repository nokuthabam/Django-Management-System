from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, StudentForm, InstructorForm
from .forms import CourseForm, SubjectForm
from .models import AdminUser, Instructor, Student
from .models import Course, Subject, Grade, Assignment
from django.contrib.auth.decorators import login_required

# Create your views here.


def signup(request):
    """
    This view will render the signup page.
    Parameters:
        request: HttpRequest object
    Returns:
        HttpResponse object
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user based on the user_type
            if form.cleaned_data['user_type'] == 'Admin':
                form.save('Admin')
                messages.success(request, 'Account created successfully.')
                return redirect('management_app:login')
            elif form.cleaned_data['user_type'] == 'Instructor':
                form.save('Instructor')
                messages.success(request, 'Account created successfully.')
                return redirect('management_app:login')
            else:
                form.save('Student')
                messages.success(request, 'Account created successfully.')
                return redirect('management_app:login')

    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    """
    This view will render the login page.
    Parameters:
        request: HttpRequest object
    Returns:
        HttpResponse object
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect based on the user type
            if AdminUser.objects.filter(user=user).exists():
                return redirect('management_app:admin_home')
            elif Instructor.objects.filter(user=user).exists():
                return redirect('management_app:index')
            else:
                return redirect('management_app:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')


def user_logout(request):
    """
    This view will log out the user.
    Parameters:
        request: HttpRequest object
    Returns:
        HttpResponse object
    """
    logout(request)
    return redirect('management_app:login')


@login_required
def index(request):
    """
    This view will render the home page.
    Parameters:
        request: HttpRequest object
    Returns:
        HttpResponse object
    """
    return render(request, 'management_app/index.html')


@login_required
def admin_home(request):
    """
    This view will render the admin home page.
    Parameters:
        request: HttpRequest object
    Returns:
        HttpResponse object
    """
    course_count = Instructor.objects.all().count()
    student_count = Student.objects.all().count()
    instructor_count = Instructor.objects.all().count()
    subject_count = Instructor.objects.all().count()

    context = {
        'course_count': course_count,
        'student_count': student_count,
        'instructor_count': instructor_count,
        'subject_count': subject_count
    }
    return render(request, 'management_app/admin_home.html', context)


# Crud operations for Course
@login_required
def course_list(request):
    """
    This view will render the course list page.
    Parameters:
        request: HttpRequest object
    Returns:
        HttpResponse object
    """
    courses = Course.objects.all()
    return render(request, 'management_app/course_list.html', {'courses': courses})


@login_required
def course_create(request):
    """
    This view will render the course create page.
    Parameters:
        request: HttpRequest object
    Returns:
        HttpResponse object
    """
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('management_app:course_list')
    else:
        form = CourseForm()
    return render(request, 'management_app/course_form.html', {'form': form})


def course_update(request, pk):
    """
    This view will render the course update page.
    Parameters:
        request: HttpRequest object
        pk: int
    Returns:
        HttpResponse object
    """
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('management_app:course_list')
    else:
        form = CourseForm(instance=course)
    return render(request, 'management_app/course_form.html', {'form': form})


def course_delete(request, pk):
    """
    This view will delete the course.
    Parameters:
        request: HttpRequest object
        pk: int
    Returns:
        HttpResponse object
    """
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('management_app:course_list')
    return render(request, 'management_app/course_confirm_delete.html', {'course': course})