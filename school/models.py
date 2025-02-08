from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)
    telegram_id = models.BigIntegerField(unique=True)
    role = models.CharField(max_length=100)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zoom_url = models.CharField(max_length=255)

class OpenSlot(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

class OfficeHour(models.Model):
    open_slot = models.ForeignKey(OpenSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    open_slot = models.ForeignKey(OpenSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)

