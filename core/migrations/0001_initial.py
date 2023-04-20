# Generated by Django 4.2 on 2023-04-20 17:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, verbose_name='ФИО')),
                ('birthday', models.DateField(verbose_name='День рождения')),
                ('phone', models.IntegerField(verbose_name='Номер телефона')),
                ('health_status', models.CharField(max_length=255, verbose_name='Описания состояния здоровья')),
            ],
            options={
                'verbose_name': 'Заявитель',
                'verbose_name_plural': 'Заявители',
                'ordering': ['full_name'],
            },
        ),
        migrations.CreateModel(
            name='EmergencyService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('service_code', models.CharField(max_length=30, verbose_name='Код службы')),
                ('phone', models.IntegerField(verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Экстренная служба',
                'verbose_name_plural': 'Экстренная служба',
                'ordering': ['service_code'],
            },
        ),
        migrations.CreateModel(
            name='Appeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True, verbose_name='Дата обращения')),
                ('number', models.IntegerField(verbose_name='Номер обращения')),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicants', to='core.applicant')),
                ('emergency_services', models.ManyToManyField(to='core.emergencyservice')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'ordering': ['date', 'number'],
            },
        ),
    ]
