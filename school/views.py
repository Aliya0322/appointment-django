from django.shortcuts import render
from django.http import HttpRequest
from .models import User


def main_page(request: HttpRequest):
    return render(request, "main_page.html")


def lesson_page(request: HttpRequest):
    return render(request, "lesson.html")


def teacher_page(request: HttpRequest):
    return render(request, "teacher.html")


def teacher_list(request):
    teachers = User.objects.filter(role='teacher')
    return render(request, 'teacher_list.html', {'teachers': teachers})


def date_page(request: HttpRequest):
    return render(request, "date_time.html")
