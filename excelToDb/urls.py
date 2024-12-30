from django.urls import path

from excelToDb.views import ExcelUploadViewSet, setDatabaseInfo, setSchedule


urlpatterns = [
    path('excel-uploads/', ExcelUploadViewSet.as_view({
             'get': 'list',
             'post': 'create'
         })),

    path('set-schedule/', setSchedule),
    path('set-database-info', setDatabaseInfo)
    
]