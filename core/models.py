import uuid

from django.db import models
from .consts import GENDER_CHOICES, STATUS_CHOICES, in_progress, GENDER_MALE


class EmergencyService(models.Model):
    title = models.CharField(
        'Название',
        max_length=255,
    )
    service_code = models.CharField(
        'Код службы',
        max_length=255,
    )
    phone = models.PositiveBigIntegerField(
        'Номер телефона',
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['service_code']
        verbose_name = 'Экстренная служба'
        verbose_name_plural = 'Экстренные службы'


class Applicant(models.Model):
    first_name = models.CharField(
        "Имя",
        max_length=255,
    )
    middle_name = models.CharField(
        "Фамилия",
        max_length=255,
    )
    last_name = models.CharField(
        "Отчество",
        max_length=255,
    )
    birthday = models.DateField(
        'День рождения',
    )
    phone = models.PositiveBigIntegerField(
        'Номер телефона',
        null=True,
        blank=True,
    )
    health_status = models.CharField(
        'Описания состояния здоровья',
        max_length=255,
        null=True,
        default='Практически здоров',
        help_text='Аллергоанамнез, хранические заболевания и т.п.',
        blank=True,
    )
    gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        default=GENDER_MALE,
    )
    image = models.ImageField(
        'Изображение',
        upload_to='images/',
        blank=True,
        null=True,
    )

    def get_gender(self):
        return self.gender

    def __str__(self):
        return f'Заявитель: {self.first_name}'

    class Meta:
        ordering = ['first_name']
        verbose_name = 'Заявитель'
        verbose_name_plural = 'Заявители'


class Appeal(models.Model):
    date = models.DateField(
        'Дата обращения',
        auto_now=True,
    )
    number = models.UUIDField(
        'Номер обращения',
        db_index=True,
        editable=False,
        unique=True,
        default=uuid.uuid4,
    )
    applicant = models.ForeignKey(  # От одного заявителя может быть много обращений
        Applicant,
        on_delete=models.CASCADE,
        related_name='appeals',
        verbose_name='Заявитель',
    )
    emergency_services = models.ManyToManyField(  # Одно обращение - одна или более экстренных служб
        EmergencyService,
        verbose_name="Экстренные службы",
    )
    status = models.CharField(
        'Статус обращения',
        max_length=255,
        choices=STATUS_CHOICES,
        default=in_progress,
    )
    victims_number = models.PositiveIntegerField(
        'Число пострадавших',
    )
    do_not_call = models.BooleanField(
        'Не звонить',
        default=False,
    )

    def __str__(self):
        return f'{self.number} ({self.applicant.first_name})'

    class Meta:
        ordering = ['date', 'number']
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
