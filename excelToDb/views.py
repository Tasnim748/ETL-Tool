import sys
from excelToDb.swaggerDocs import ExcelUploadRequest, ExcelUploadResponse
# from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import viewsets, status
from rest_framework.response import Response

from excelToDb.models import ExcelUpload
from excelToDb.serializers import ExcelUploadCreateSerializer, ExcelUploadViewSerializer

from drf_spectacular.utils import extend_schema

from excelToDb.utils.parseJson import parse_array_of_objects


# Create your views here.

@extend_schema(
    tags=['Excel File Uploads'],
)
class ExcelUploadViewSet(viewsets.ModelViewSet):
    queryset = ExcelUpload.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExcelUploadViewSerializer  # Use Retrieve Serializer for GET
        return ExcelUploadCreateSerializer  # Use Create Serializer for POST/PUT
    
    @extend_schema(
        summary="List all excel file uploads",
        description="Retrieve a list of all excel file upload records.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Upload a document",
        description="Upload a new document file",
        request=ExcelUploadRequest,
        responses=ExcelUploadResponse
    )
    def create(self, request):
        # preparing the fields in proper format
        file = request.FILES.get('file')
        sheet_name = request.data.get('sheet_name')

        if " " in file.name or " " in sheet_name:
            return Response(
                {"error": "no space allowed in filename or sheetname"},
                status=status.HTTP_400_BAD_REQUEST
            )

        
        try:            
            columns = parse_array_of_objects(request.data.get('columns'))
            print("columns:", columns)
            # Prepare data for serializer
            data = {
                'file': file,
                'sheet_name': sheet_name,
                'columns': columns
            }

            if request.data.get('schedule'):
                data['schedule'] = parse_datetime(request.data.get('schedule'))
            
            print('data:', data)
            serializer = self.get_serializer(data=data)
            serializer.is_valid()
            self.perform_create(serializer)
            
            print(serializer)
            return Response(
                data={"message": "File uploaded successfully"},
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            print(f"Error occurred on line {sys.exc_info()[-1].tb_lineno}: {str(e)}")
            print(e)
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )