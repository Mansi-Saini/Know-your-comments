# Generated by Django 4.1.4 on 2023-01-14 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.CharField(default='0', max_length=20),
        ),
    ]
