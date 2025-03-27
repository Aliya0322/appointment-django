from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from school.views import (
    MainPageView,
    LessonPageView,
    TeacherListView,
    DatePageView,
    BookSlotView,
    confirmation_page
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPageView.as_view(), name='main_page'),
    path('lesson/', LessonPageView.as_view(), name="lesson_page"),
    path('teacher/', TeacherListView.as_view(), name="teacher_page"),
    path('date/<int:pk>/', DatePageView.as_view(), name="date_page"),
    path('confirmation/', confirmation_page, name='confirmation_page'),
    path("book/", BookSlotView.as_view() , name = "book_slot")
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)