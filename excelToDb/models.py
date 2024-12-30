from django.db import models

# Create your models here.
class ExcelUpload(models.Model):
    file = models.FileField(upload_to='excel_uploads/')
    sheet_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    table_name = models.CharField(max_length=255)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.table_name} (id={self.id})"



class Column(models.Model):
    excel_upload = models.ForeignKey(
        ExcelUpload,
        on_delete=models.CASCADE,
        related_name='columns'
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.excel_upload.sheet_name})"



class Schedule(models.Model):
    excel_upload = models.OneToOneField(
        ExcelUpload,
        on_delete=models.CASCADE,
        related_name='schedule'
    )
    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_executed = models.BooleanField(default=False)

    def __str__(self):
        return f"Schedule for {self.excel_upload.sheet_name} (id={self.id})"
    

class DatabaseInfo(models.Model):
    excel_upload = models.OneToOneField(
        ExcelUpload,
        on_delete=models.CASCADE,
        related_name='databaseinfo'
    )
    server_ip = models.CharField(max_length=255, null=True, blank=True)
    database_name = models.CharField(max_length=255, null=True, blank=True)
    table_name = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.server_ip} {self.table_name}"
    
    def save(self, *args, **kwargs):
        if not self.table_name:
            self.table_name = f"{self.excel_upload.file.name.replace('/', '.').split('.')[1].lower()}_{self.excel_upload.sheet_name}"
        super().save(*args, **kwargs)