from django.contrib import admin

from excelToDb.inlines import ColumnInline, ScheduleInline
from excelToDb.models import ExcelUpload, Schedule

admin.site.register(Schedule)

# Register your models here.
@admin.register(ExcelUpload)
class ExcelUploadAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline, ColumnInline]
    list_display = ['sheet_name']