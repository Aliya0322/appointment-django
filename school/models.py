from django.db import models

class UserManager(models.Manager):
    def get_students(self):
        return self.get_queryset().filter(role='student')

    def get_teachers(self):
        return self.get_queryset().filter(role='teacher')

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    name = models.CharField(max_length=255, verbose_name="Имя")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Номер телефона")
    telegram_id = models.IntegerField(verbose_name="Телеграм ID")
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, verbose_name="Роль")

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == 'teacher' and not Teacher.objects.filter(user=self).exists():
            Teacher.objects.create(user=self)

    def __str__(self):
        return self.name


    class Meta:
        db_table = "user"
        indexes = [models.Index(fields=['name'])]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"




class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    zoom_url = models.URLField(max_length=200, verbose_name="Ссылка на Zoom")

    objects = models.Manager()

    def __str__(self):
        return f'Teacher: {self.user.name}'

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class OpenSlot(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")

    objects = models.Manager()

    def __str__(self):
        return f'{self.date} {self.time} - {self.teacher.user.name}'

    class Meta:
        verbose_name = "Открытый слот"
        verbose_name_plural = "Открытые слоты"


class OfficeHour(models.Model):
    open_slot = models.ForeignKey(OpenSlot, on_delete=models.CASCADE, verbose_name="Открытый слот")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    objects = models.Manager()

    def __str__(self):
        return f'OfficeHour: {self.open_slot} with {self.user.name}'

    class Meta:
        verbose_name = "Часы приема"
        verbose_name_plural = "Часы приема"


class Booking(models.Model):
    STATUS_CHOICES = [
        ("confirmed", "Подтвержден"),
        ("cancelled", "Отменен"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    open_slot = models.OneToOneField(OpenSlot, on_delete=models.CASCADE, verbose_name="Открытый слот")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Статус бронирования", default="confirmed")

    objects = models.Manager()

    def __str__(self):
        return f'Booking: {self.user.name} - {self.open_slot} ({self.status})'

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"






