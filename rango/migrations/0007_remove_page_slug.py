# Generated by Django 2.1.5 on 2020-02-02 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_auto_20200202_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='slug',
        ),
    ]
