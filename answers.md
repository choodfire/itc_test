# Ответы на вопросы

---

## Сохранение объектов в БД

1. Сохраните несколько объектов модели "Экстренных служб", "Заявителя" и "Обращения" двумя способами (методом create
уровня менеджера запросов objects и методом save уровня экземпляра модели)

```
es1 = EmergencyService(title="Полиция", service_code='02', phone='02')
es1.save()
es2 = EmergencyService(title="Скорая помощь", service_code='03', phone='03')
es2.save()
EmergencyService.objects.create(title="Пожарная", service_code='01', phone='01')

Applicant.objects.create(first_name='Руслан', middle_name='Русланов', last_name='Русланович', birthday=datetime.date(2002, 8, 26), gender='M')
apl = Applicant(first_name='Дмитрий', middle_name='Дмитриев', last_name='Дмитриевич', birthday=datetime.date(1995, 1, 26), gender='М', health_status='Полностью здоров', phone=88005553535)
apl.save()

Appeal.objects.create(applicant_id=1, number=1, status='В работе', victims_number=1, do_not_call=True)
appeal = Appeal(applicant=apl, do_not_call=False, status='Завершено', victims_number=123, number=2)
appeal.save()
```

2. Создайте "Обращение" через менеджер запросов от объекта "Заявитель"

```
a = Applicant.objects.get(id=1)
e = a.appeals.create(do_not_call=False, status='Завершено', victims_number=123, number=3)
```

3. Добавьте "Обращению" несколько "экстренных служб" двумя способами (add, set)

```
es1 = EmergencyService.objects.get(id=1)
es2 = EmergencyService.objects.get(id=2)
es3 = EmergencyService.objects.get(id=3)
appeal = Appeal.objects.get(id=1)
appeal.emergency_services.add(es1)

appeal = Appeal.objects.get(id=2)
appeal.emergency_services.set([es1,es2,es3])
```

---

## Запросы в БД

1. Получить объект заявителя с идентификатором в базе данных = 1 тремя способами.

```
Applicant.objects.get(id=1)
Applicant.objects.get(id__exact=1)
Applicant.objects.get(pk=1)
```

2. Получить все обращения заявителя двумя способами

```
a = Applicant.objects.get(id=1)

1. Appeal.objects.filter(applicant=a)
2. a.appeals.all()
```

3. Получить первые три экстренные службы

```
EmergencyService.objects.all()[:3]
```

4. Получить последние пять заявителей

```
Applicant.objects.all().order_by('-id')[:5]
```

5. Получить самое старое и самое новое обращение двумя способами (latest, earliest, order_by)

```
Appeal.objects.earliest('date')
Appeal.objects.latest('date')

Appeal.objects.order_by('date').first()
Appeal.objects.order_by('date').last()
```

6. Получить каждое второе обращение

```
Appeal.objects.all()[1::2]
```

7. Если дважды проитерироваться по полученному QuerySet`y, то сколько будет сделано обращений в БД? С помощью конструкции len(connection.queries) можно проверить количество запросов в БД. Для сброса следует использовать reset_queries() из django.db.

```
2 запроса

reset_queries()
len(connection.queries)
0
for i in a.iterator():
    print(i)
...
1
2
3
len(connection.queries)
1
for i in a.iterator():
    print(i)
...
1
2
3
len(connection.queries)
2
```

8. Вывести общее число обращений

```
Appeal.objects.count()
```

9. Получить случайное обращение

```
Appeal.objects.order_by('?').first()
```

---

## Фильтрация

1. Получить обращение с заявителем, идентификатор которого равен 1

```
Appeal.objects.filter(applicant_id=1)  # .first если одно
```

2. Получить всех заявителей определенного пола и без обращений

```
Applicant.objects.filter(gender='М', appeals__isnull=True)
```

3. Отсортировать всех заявителей по идентификатору

```
Applicant.objects.all().order_by('id')
```

4. Получить всех несовершеннолетних заявителей

```
Applicant.objects.filter(birthday__gt=(datetime.date.today() - relativedelta(years=18)))
```

5. Получить всех совершеннолетних заявителей 

```
Applicant.objects.filter(birthday__lt=(datetime.date.today() - relativedelta(years=18)))
```

6. Узнать есть ли вообще какие нибудь заявители

```
Applicant.objects.exists()
```

7. Узнать, есть ли какие нибудь заявители с похожими именами (пример: Алексей, Александра)

```
Applicant.objects.filter(first_name__contains='алекс')
```

8. Получить все обращения, кроме тех, у которых не назначены службы

```
Appeal.objects.exclude(emergency_services__isnull=True)
```

9. Среди обращений со службой с кодом "03" вывести дату самого первого обращения 

```
Appeal.objects.filter(emergency_services__service_code='03').values('date').earliest('date')
```

10. Получить все обращения, которые созданы до определенной даты

```
Appeal.objects.filter(date__lt=datetime.date.today())
```

11. Получить всех заявителей без изображения и/или без номера телефона

```
Applicant.objects.filter(phone__isnull=True, image__isnull=True)  # Либо если image не может быть null - Applicant.objects.filter(phone__isnull=True, image="")
Applicant.objects.filter(Q(phone__isnull=True) | Q(image__isnull=True))
```

12. Получить всех заявителей, с определенным кодом оператора (917)

```
Applicant.objects.filter(phone__startswith='917')
```

13. Получить результат объединения, пересечения и разницы предыдущих двух запросов.

```
qs1.union(qs2)
qs1.intersection(qs2)
qs1.difference(qs2)
```

14. Вывести все обращения, созданные в определенный период

```
start = datetime.date.today() - relativedelta(years=18)
end = datetime.date.today()
Appeal.objects.filter(date__range=(start, end))
```

15. Получить количество заявителей без номера телефона

```
Applicant.objects.filter(phone__isnull=True).count()  # Либо phone=""
```

16. Выведите все уникальные записи модели заявитель 

```
Applicant.objects.distinct()
```

17. Получить все обращения, в описании которых есть какое то ключевое слово в любом регистре номер

```
Appeal.objects.filter(status__isnull=False)  # ~status=""
```

18. Выбрать всех заявителей, при этом получить только значения поля "номер телефона"

```
Applicant.objects.all().values('phone')
```

19. Выбрать всех заявителей, при этом получить все поля, кроме состояния здоровья 

```
Applicant.objects.all().defer('health_status')
```

20. Вывести все службы используя sql запрос

```
EmergencyService.objects.raw("SELECT * FROM core_emergencyservice")
```

21. Выберите или создайте заявителя с номером "12341234"

```
Applicant.objects.get_or_create(phone=12341234, defaults={"birthday": datetime.date(1940, 10, 9)})
```

22. Измените номер заявителя с номером "12341234" на любой другой, если заявителя, то запрос должен его создать.

```
Applicant.objects.update_or_create(phone=12341234, defaults={"phone": 1234})
```

23. Создайте сразу несколько заявителей.

```
objs = Applicant.objects.bulk_create(
    [
        Applicant(first_name='Максим', middle_name='Максимов', last_name='Максимович', birthday=datetime.date(1976, 10, 9), gender='М', phone=123456),
        Applicant(first_name='Роман', middle_name='Романов', last_name='Романович', birthday=datetime.date(2001, 10, 9), gender='М', phone=87654),
    ]
)
```

24. Измените несколько заявителей. Для поля "состояние здоровья" задайте значение "Полностью здоров"

```
applicants = Applicant.objects.filter(id__in=[5,6])
applicants = list(applicants)
applicants
[<Applicant: Максимов Максим Максимович>, <Applicant: Романов Роман Романович>]
for applicant in applicants:
    applicant.health_status = 'Полностью здоров'

Applicant.objects.bulk_update(applicants, ['health_status'])
```

25. Выведите имя заявителя у какого-либо обращения. Убедитесь, что было сделано не более одного запроса.

```
Appeal.objects.order_by('?').values_list('applicant__first_name', flat=True).first()
```

26. Выведите список всех обращений с указанием списка задействованных экстренных служб в следующем формате: " обращения:, список кодов служб:. Убедитесь, что было сделано не более двух запросов в БД.

```
apls = list(Appeal.objects.all().prefetch_related('emergency_services').values('id', 'emergency_services'))

amounts = {}

for apl in apls:
    if apl['emergency_services'] is None:
        continue

    if apl['id'] in amounts:
        amounts[apl['id']].append(apl['emergency_services'])
    else:
        amounts[apl['id']] = [apl['emergency_services']]

for key in amounts:
    print(f'{key}: {amounts[key]}')
```

27. Выведите все значения дат создания происшествий. Поместите даты в список.

```
list(Appeal.objects.all().values_list('date', flat=True))
```

28. Создайте queryset, который будет всегда пустым.

```
Appeal.objects.none()
```

29. Вывести среднее количество пострадавших в происшествиях

```
from django.db.models import Avg
Appeal.objects.aggregate(Avg('victims_number'))
```

30. Вывести общее количество пострадавших в происшествиях

```
from django.db.models import Sum
Appeal.objects.aggregate(Sum('victims_number'))
```

31. Вывести количество вызванных экстренных служб для каждого происшествия

```
a = Appeal.objects.annotate(Count('emergency_services'))
appeals = Appeal.objects.annotate(Count('emergency_services'))
for a in appeals:
    print(f'На {a.id} обращение приехало {a.emergency_services__count} служб')
```

32. Вывести среднее количество вызванных экстренных служб

```
Appeal.objects.aggregate(Avg('emergency_services'))
```

33. Вывести наибольшее и наименьшее количество пострадавших

```
from django.db.models import Max, Min
Appeal.objects.aggregate(Max('victims_number'))
Appeal.objects.aggregate(Min('victims_number'))
```

34. Сформировать запрос к модели заявитель, в котором будет добавлено поле с количеством обращений каждого заявителя.

```
apl = Applicant.objects.annotate(amount = Count('appeals'))
for a in apl:
    print(f'{a.first_name} - {a.amount}')
```

### Дополнительно

1. Всем обращениям, у которых назначены службы, присвоить статус "Завершено"

```
Appeal.objects.filter(emergency_services__isnull=True).update(status='Завершено')
```

2. Удалить всех заявителей без номера телефона

```
Applicant.objects.filter(phone__isnull=True).delete()
```
