# Generated by Django 3.2 on 2021-07-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0016_auto_20210701_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='slug',
            field=models.SlugField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(),
        ),
    ]
