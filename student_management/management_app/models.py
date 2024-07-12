from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Course(models.Model):
    """
    Model representing a course.
    Attributes:
        id (int): The course's unique identifier.
        name (str): The course's name.
        description (str): The course's description.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    """
    Model representing a subject.
    Attributes:
        id (int): The subject's unique identifier.
        name (str): The subject's name.
        course (Course): The course to which the subject belongs.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class AdminUser(models.Model):
    """
    Model representing an admin user.
    Attributes:
        user (User): The user object associated with the admin user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100, default='Admin')
    
    def __str__(self):
        return self.user.username


class Student(models.Model):
    """
    Model representing a student.
    Attributes:
        id (int): The student's unique identifier.
        name (str): The student's name.
        email (str): The student's email address.
        course (Course): The course to which the student belongs.
        subjects (list of Subject): The student's subjects.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    subjects = models.ManyToManyField(Subject)
    user_type = models.CharField(max_length=100, default='student')

    def __str__(self):
        return self.user.username


class Instructor(models.Model):
    """
    Model representing an instructor.
    Attributes:
        id (int): The instructor's unique identifier.
        name (str): The instructor's name.
        email (str): The instructor's email address.
        course (Course): The course to which the instructor belongs.
        subject (Subject): The subject the instructor teaches.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=100, default='instructor')

    def __str__(self):
        return self.user.username


class Assignment(models.Model):
    """
    Model representing an assignment.
    Attributes:
        id (int): The assignment's unique identifier.
        title (str): The assignment's name.
        description (str): The assignment's description.
        due_date (datetime): The assignment's due date.
        subject (Subject): The subject to which the assignment belongs.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Grade(models.Model):
    """
    Model representing a grade.
    Attributes:
        id (int): The grade's unique identifier.
        student (Student): The student who received the grade.
        subject (Subject): The subject for which the grade was given.
        assignment (Assignment): The assignment for which the grade was given.
        grade (float): The grade value.
    """
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    grade = models.FloatField()

    def __str__(self):
        return str(self.grade)
