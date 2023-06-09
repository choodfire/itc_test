# Generated by Django 4.2 on 2023-04-20 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appeal',
            name='do_not_call',
            field=models.BooleanField(default=False, verbose_name='Не звонить'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='status',
            field=models.CharField(choices=[('В работе', 'В работе'), ('Завершено', 'Завершено')], default='В работе', max_length=9, verbose_name='Статус обращения'),
        ),
        migrations.AddField(
            model_name='appeal',
            name='victims_number',
            field=models.IntegerField(default=-1, verbose_name='Число пострадавших'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicant',
            name='gender',
            field=models.CharField(choices=[('М', 'Мужской'), ('Ж', 'Женский')], default=1, max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='applicant',
            name='image',
            field=models.ImageField(default='no image', upload_to='images/', verbose_name='Изображение'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='appeal',
            name='number',
            field=models.IntegerField(db_index=True, editable=False, unique=True, verbose_name='Номер обращения'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='health_status',
            field=models.CharField(default='Практически здоров', help_text='Аллергоанамнез, хранические заболевания и т.п.', max_length=255, null=True, verbose_name='Описания состояния здоровья'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='phone',
            field=models.IntegerField(null=True, verbose_name='Номер телефона'),
        ),
    ]
