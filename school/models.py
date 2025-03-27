from django.db import models


class UserManager(models.Manager):
    def create_user(self, telegram_id, first_name="Без имени", last_name="", role="student"):
        if not telegram_id:
            raise ValueError("Пользователь должен иметь Telegram ID")
        user = self.model(
            telegram_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, first_name, last_name=""):
        user = self.create_user(telegram_id, first_name, last_name, role="admin")
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_students(self):
        return self.get_queryset().filter(role="student")

    def get_teachers(self):
        return self.get_queryset().filter(role="teacher")


class User(models.Model):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]
    first_name = models.CharField(max_length=255, verbose_name="Имя", blank=True, null=True)
    last_name = models.CharField(max_length=255, verbose_name="Фамилия", blank=True, null=True)
    middle_name = models.CharField(max_length=255, verbose_name="Отчество", blank=True, null=True)
    telegram_id = models.IntegerField(verbose_name="Телеграм ID", unique=True)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, verbose_name="Роль")

    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.role == "teacher":
            Teacher.objects.get_or_create(user=self)
        else:
            Teacher.objects.filter(user=self).delete()

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}".strip()

    class Meta:
        db_table = "user"
        indexes = [models.Index(fields=["last_name"])]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name="Пользователь")
    zoom_url = models.URLField(max_length=200, verbose_name="Ссылка на Zoom", blank=True, null=True)
    photo = models.ImageField(upload_to="teachers_photos/", blank=True, null=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name} {self.user.middle_name or ''}".strip()

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"


class OpenSlot(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")

    objects = models.Manager()

    def __str__(self):
        return f"{self.date} {self.time} - {self.teacher.user.last_name} {self.teacher.user.first_name}".strip()

    class Meta:
        verbose_name = "Открытый слот"
        verbose_name_plural = "Открытые слоты"


class OfficeHour(models.Model):
    open_slot = models.ForeignKey(OpenSlot, on_delete=models.CASCADE, verbose_name="Открытый слот")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")

    objects = models.Manager()

    def __str__(self):
        return f"OfficeHour: {self.open_slot} with {self.user.last_name} {self.user.first_name}".strip()

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
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name="Статус бронирования",
                              default="confirmed")

    objects = models.Manager()

    def __str__(self):
        return f"Booking: {self.user.last_name} {self.user.first_name} - {self.open_slot} ({self.status})".strip()

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

