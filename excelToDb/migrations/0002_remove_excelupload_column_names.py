# Generated by Django 5.1.4 on 2024-12-22 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excelToDb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='excelupload',
            name='column_names',
        ),
    ]