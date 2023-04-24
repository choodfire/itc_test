GENDER_MALE = ('М', 'Мужской')
GENDER_FEMALE = ('Ж', 'Женский')

GENDER_CHOICES = [
    GENDER_MALE,
    GENDER_FEMALE,
]

in_progress = 'В работе'
finished = 'Завершено'
STATUS_CHOICES = [
    (in_progress, in_progress),
    (finished, finished),
]
