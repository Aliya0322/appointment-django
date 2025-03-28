from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.decorators import method_decorator
from datetime import timedelta
import json
from babel.dates import format_date
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Teacher, OpenSlot, Booking


class MainPageView(View):
    @staticmethod
    def get(request: HttpRequest):
        return render(request, "main_page.html")


class LessonPageView(View):
    @staticmethod
    def get(request: HttpRequest):
        return render(request, "lesson.html")

@api_view(["GET"])
def get(request:HttpRequest, user_id):
    bookings = Booking.objects.filter(
        user__telegram_id=user_id
    ).order_by('-date')

    data = {
        "past" : [],
        "future": []
    }
    current_date = now()

    for booking in bookings:
        booking_data = {
            "id" : booking.id,
            "date": booking.open_slot.date,
            "time": booking.open_slot.time,
            "name": booking.user.name, #имя педагога
        }
        if booking.open_slot.date < current_date:
            data["past"].append(booking_data)
        else:
            data["future"].append(booking_data)
    return Response(data)


class TeacherListView(ListView):
    model = User
    template_name = "teacher.html"
    context_object_name = 'teachers'

    def get_queryset(self):
        return User.objects.filter(role='teacher').select_related('teacher')


class DatePageView(DetailView):
    model = Teacher
    template_name = 'date_time.html'
    context_object_name = 'teacher'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = timezone.now().date()
        next_7_days = [today + timedelta(days=i) for i in range(7)]

        # Получаем забронированные слоты (у которых статус "confirmed")
        booked_slots = Booking.objects.filter(status="confirmed").values_list("open_slot_id", flat=True)

        # Фильтруем только свободные слоты
        open_slots = OpenSlot.objects.filter(
            teacher=self.object,
            date__gte=today,
            date__lte=today + timedelta(days=6)
        ).exclude(id__in=booked_slots).order_by('date', 'time')

        active_dates = set(slot.date for slot in open_slots)

        context['current_month'] = format_date(today, "LLLL Y", locale='ru')
        context['next_7_days'] = [
            {
                'date': date,
                'is_active': date in active_dates
            }
            for date in next_7_days
        ]
        context['open_slots'] = open_slots  # Передаем только свободные слоты

        return context



def confirmation_page(request):
    slot_id = request.GET.get('slot_id')
    slot = get_object_or_404(OpenSlot, id=slot_id)
    teacher = slot.teacher
    selected_date = slot.date
    selected_time = slot.time.strftime('%H:%M')

    user = request.user

    context = {
        'teacher': teacher,
        'slot': slot,
        'user': user,
        'selected_date': selected_date,
        'selected_time': selected_time,
    }
    return render(request, 'confirmation.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class BookSlotView(View):
    @staticmethod
    def post(request):
        slot_id = request.POST.get("slot_id")
        user_id = request.POST.get("user_id")

        if not slot_id or not user_id:
            return JsonResponse({"error": "Не указан слот или пользователь"}, status=400)

        try:
            slot = OpenSlot.objects.get(id=slot_id)
        except OpenSlot.DoesNotExist:
            return JsonResponse({"error": "Слот не найден"}, status=404)

        user = User.objects.get(id=user_id)

        booking = Booking.objects.create(
            user=user,
            open_slot=slot,
            status="confirmed",
        )

        return JsonResponse({"message": "Запись успешно создана!",  "booking_id": booking.id})


    @staticmethod
    def get(self, request):
        return JsonResponse({"error": "Некорректный запрос"}, status=400)


@csrf_exempt
def cancel_lesson(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lesson_id = data.get("lesson_id")

            lesson = Booking.objects.get(id=lesson_id)
            lesson.delete()

            return JsonResponse({"success": True})
        except Booking.DoesNotExist:
            return JsonResponse({"success": False, "error": "Занятие не найдено"}, status=404)

    return JsonResponse({"success": False, "error": "Неверный запрос"}, status=400)


