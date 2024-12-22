from django.db import models

# Create your models here.
class ExcelUpload(models.Model):
    file = models.FileField(upload_to='excel_uploads/')
    sheet_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    table_name = models.CharField(max_length=255)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.table_name



class Column(models.Model):
    excel_upload = models.ForeignKey(
        ExcelUpload,
        on_delete=models.CASCADE,
        related_name='columns'
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.excel_upload.sheet_name}"



class Schedule(models.Model):
    excel_upload = models.OneToOneField(
        ExcelUpload,
        on_delete=models.CASCADE,
        related_name='schedule'
    )
    scheduled_at = models.DateTimeField()
    is_executed = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for {self.excel_upload.sheet_name}"