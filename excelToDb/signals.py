import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from excelToDb.models import ExcelUpload


@receiver(post_delete, sender=ExcelUpload)
def auto_delete_file_on_delete(sender, instance: ExcelUpload, **kwargs):
    if instance.file:
        print(instance.file.path)
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)