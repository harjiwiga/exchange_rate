# Generated by Django 2.1 on 2018-08-04 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchangerateapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchangerate',
            name='date',
            field=models.DateField(null=True),
        ),
    ]