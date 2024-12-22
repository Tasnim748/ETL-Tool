from django.contrib import admin
from excelToDb.models import Column, Schedule


class ScheduleInline(admin.TabularInline):
    model = Schedule



class ColumnInline(admin.TabularInline):
    model = Column
    extra = 1