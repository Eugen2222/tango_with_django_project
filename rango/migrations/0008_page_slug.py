# Generated by Django 2.1.5 on 2020-02-02 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0007_remove_page_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='slug',
            field=models.SlugField(default=''),
            preserve_default=False,
        ),
    ]
