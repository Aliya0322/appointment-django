from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.utils import timezone
from django.utils.decorators import method_decorator
from datetime import timedelta
import json
from babel.dates import format_date
from .models import User, Teacher, OpenSlot, Booking


class MainPageView(View):
    def get(self, request: HttpRequest):
        return render(request, "main_page.html")


class LessonPageView(View):
    def get(self, request: HttpRequest):
        return render(request, "lesson.html")


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
    teacher = slot.teacher  # Предполагаем, что есть связь с преподавателем
    selected_date = slot.date  # Дата занятия
    selected_time = slot.time.strftime('%H:%M')  # Время занятия

    context = {
        'teacher': teacher,
        'slot': slot,
        'selected_date': selected_date,
        'selected_time': selected_time,
    }
    return render(request, 'confirmation.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class BookSlotView(View):
    @staticmethod
    def post(request):
        slot_id = request.POST.get("slot_id")

        if not slot_id:
            return JsonResponse({"error": "Не указан слот"}, status=400)

        return JsonResponse({"message": "Запись успешно создана!"})

    @staticmethod
    def get(request):
        return JsonResponse({"error": "Некорректный запрос"}, status=400)

@csrf_exempt
def telegram_auth(request):
    telegram_id = request.GET.get("id")
    first_name = request.GET.get("first_name", " ")

    if not telegram_id:
        return JsonResponse({"error": "Нет данных от Telegram"}, status=400)

    user, created = User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={"name": first_name, "role": "student"}
    )

    login(request, user)

    return JsonResponse({"message": "Успешный вход!", "created": created})


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


