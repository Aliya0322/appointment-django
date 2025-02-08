from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from school.views import main_page, lesson_page, teacher_page, teacher_list, date_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main-page'),
    path('lesson/', lesson_page, name="lesson-page"),
    path('teacher/', teacher_page, name="teacher-page"),
    path('teachers/', teacher_list, name='teacher_list'),
    path('date/', date_page, name="date-page"),


]
