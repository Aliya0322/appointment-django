from django.contrib import admin

from school.models import User, Teacher, OpenSlot, OfficeHour, Booking


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'telegram_id', 'role')
    list_filter = ("role",)
    search_fields = ('last_name', "telegram_id")
    list_display_labels = {
        "name": "Имя",
        "telegram_id": "Telegram ID",
        "role": "Роль",
    }


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user", "zoom_url")
    list_display_labels = {
        "user": "Пользователь",
        "zoom_url": "Ссылка на Zoom",
    }
    search_fields = ("user__last_name",)

@admin.register(OpenSlot)
class OpenSlotAdmin(admin.ModelAdmin):
    list_display = ("teacher", "date", "time")
    list_filter = ("date", "teacher")
    date_hierarchy = "date"
    list_display_labels = {
        "teacher": "Преподаватель",
        "date": "Дата",
        "time": "Время",
    }

@admin.register(OfficeHour)
class OfficeHourAdmin(admin.ModelAdmin):
    list_display = ("open_slot", "user")
    list_display_labels = {
        "open_slot": "Открытый слот",
        "user": "Пользователь",
    }
    list_filter = ("open_slot__date", "user")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "open_slot", "status")
    list_filter = ("status",)
    actions = ["mark_as_confirmed", "mark_as_cancelled"]
    list_display_labels = {
        "user": "Пользователь",
        "open_slot": "Открытый слот",
        "status": "Статус",
    }

    def mark_as_confirmed(self, request, queryset):
        queryset.update(status="confirmed")

    mark_as_confirmed.short_description = "Отметить как подтвержденные"

    def mark_as_cancelled(self, request, queryset):
        queryset.update(status="cancelled")

    mark_as_cancelled.short_description = "Отметить как отмененные"





