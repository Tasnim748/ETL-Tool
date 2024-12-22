from django.urls import path

from excelToDb.views import ExcelUploadViewSet


urlpatterns = [
    path('', ExcelUploadViewSet.as_view({
             'get': 'list',
             'post': 'create'
         })),
]