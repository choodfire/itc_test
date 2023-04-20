from django.db import models


class EmergencyService(models.Model):
    title = models.CharField(
        'Название',
        max_length=255,
    )
    service_code = models.CharField(
        'Код службы',
        max_length=30,
    )
    phone = models.IntegerField(
        'Номер телефона',
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['service_code']
        verbose_name = 'Экстренная служба'
        verbose_name_plural = 'Экстренная служба'


class Applicant(models.Model):
    full_name = models.CharField(
        'ФИО',
        max_length=255,
    )
    birthday = models.DateField(
        'День рождения',
    )
    phone = models.IntegerField(
        'Номер телефона',
        null=True,
    )
    health_status = models.CharField(
        'Описания состояния здоровья',
        max_length=255,
        null=True,
        default='Практически здоров',
        help_text='Аллергоанамнез, хранические заболевания и т.п.',
    )
    GENDER_CHOICES = [
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
    )
    image = models.ImageField(  # todo check
        'Изображение',
        upload_to='images/',
    )

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Заявитель'
        verbose_name_plural = 'Заявители'


class Appeal(models.Model):
    date = models.DateField(
        'Дата обращения',
        auto_now=True,
    )
    number = models.IntegerField(
        'Номер обращения',
        db_index=True,
        editable=False,
        unique=True,
    )
    applicant = models.ForeignKey(  # От одного заявителя может быть много обращений
        Applicant,
        on_delete=models.CASCADE,
        related_name='applicants'
    )
    emergency_services = models.ManyToManyField(  # Одно обращение - одна или более экстренных служб
        EmergencyService,
    )
    in_progress = 'В работе'
    finished = 'Завершено'
    STATUS_CHOICES = [
        (in_progress, in_progress),
        (finished, finished),
    ]
    status = models.CharField(
        'Статус обращения',
        max_length=9,
        choices=STATUS_CHOICES,
        default=in_progress,
    )
    victims_number = models.IntegerField(
        'Число пострадавших',
    )
    do_not_call = models.BooleanField(
        'Не звонить',
        default=False,
    )

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['date', 'number']
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
