# Generated by Django 2.1 on 2018-08-04 15:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exchangerateapp', '0003_auto_20180804_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerate',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
