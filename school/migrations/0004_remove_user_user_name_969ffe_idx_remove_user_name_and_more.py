# Generated by Django 5.1.5 on 2025-03-26 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_booking_options_alter_officehour_options_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='user',
            name='user_name_969ffe_idx',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Фамилия'),
        ),
        migrations.AddField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Отчество'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['last_name'], name='user_last_na_26742a_idx'),
        ),
    ]
