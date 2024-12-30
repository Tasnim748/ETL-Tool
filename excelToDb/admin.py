from django.contrib import admin

from excelToDb.inlines import ColumnInline, ScheduleInline
from excelToDb.models import DatabaseInfo, ExcelUpload, Schedule

admin.site.register(Schedule)
admin.site.register(DatabaseInfo)

# Register your models here.
@admin.register(ExcelUpload)
class ExcelUploadAdmin(admin.ModelAdmin):
    inlines = [ScheduleInline, ColumnInline]
    list_display = ['id', 'sheet_name']