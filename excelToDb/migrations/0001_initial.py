# Generated by Django 5.1.4 on 2024-12-22 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='excel_uploads/')),
                ('sheet_name', models.CharField(max_length=255)),
                ('column_names', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('table_name', models.CharField(max_length=255, unique=True)),
                ('is_processed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_at', models.DateTimeField()),
                ('is_executed', models.BooleanField(default=False)),
                ('excel_upload', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to='excelToDb.excelupload')),
            ],
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('excel_upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='excelToDb.excelupload')),
            ],
            options={
                'unique_together': {('excel_upload', 'name')},
            },
        ),
    ]