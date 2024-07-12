from django.contrib import admin
from .models import Course, Subject, Student, Instructor, Assignment, Grade, AdminUser

# Register your models here.
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Assignment)
admin.site.register(Grade)
admin.site.register(AdminUser)
