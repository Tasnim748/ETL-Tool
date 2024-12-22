import json
import sys
from django.shortcuts import render
from django.utils.dateparse import parse_datetime
from django.utils import timezone

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser

import pandas as pd

from excelToDb.models import ExcelUpload
from excelToDb.serializers import ExcelUploadCreateSerializer, ExcelUploadViewSerializer

class ExcelUploadViewSet(viewsets.ModelViewSet):
    queryset = ExcelUpload.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExcelUploadViewSerializer  # Use Retrieve Serializer for GET
        return ExcelUploadCreateSerializer  # Use Create Serializer for POST/PUT

    def create(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        sheet_name = request.data.get('sheet_name')
        columns = request.data.get('columns')
        schedule = parse_datetime(request.data.get('schedule'))
        schedule = timezone.make_aware(schedule)

        print('request:', request.data)
        
        column_names = []
        if 'columns' in request.data:
            # Try to handle both string and list inputs
            if isinstance(request.data['columns'], str):
                try:
                    # Try to parse if it's a JSON string
                    column_names = json.loads(request.data['columns'])
                except json.JSONDecodeError:
                    # If not JSON, split by comma
                    column_names = [col.strip() for col in request.data['columns'].split(',')]
            else:
                column_names = request.data['columns']


        print("column names from request:", column_names)
        print('schedule:', type(schedule))
        
        try:
            # Validate the Excel file and sheet name
            df = pd.read_excel(file, sheet_name=sheet_name)
            available_columns = df.columns.tolist()
            
            print('available columns in sheet:', available_columns)
            # Validate requested columns exist in the sheet
            if not all(col in available_columns for col in column_names):
                return Response(
                    {"error": "Some requested columns do not exist in the sheet"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Prepare data for serializer
            data = {
                'file': file,
                'sheet_name': sheet_name,
                'columns': columns
            }

            
            if schedule:
                data['schedule'] = schedule
            
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
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )