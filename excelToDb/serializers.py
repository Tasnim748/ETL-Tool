from rest_framework import serializers
from excelToDb.models import Column, ExcelUpload, Schedule
import pandas as pd

from excelToDb.tasks import trigger_schedule
from excelToDb.utils.runSchedule import run_schedule

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['name', 'type']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['scheduled_at']


class ExcelUploadViewSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(required=False)
    columns = ColumnSerializer(required=False, many=True)
    class Meta:
        model = ExcelUpload
        fields = ['id', 'file', 'sheet_name', 'columns', 'schedule', 'table_name']


class ExcelUploadCreateSerializer(serializers.ModelSerializer):
    schedule = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])
    columns = ColumnSerializer(many=True)

    class Meta:
        model = ExcelUpload
        fields = ['id', 'file', 'sheet_name', 'columns', 'schedule']

    def create(self, validated_data):
        columns = validated_data.pop('columns')
        schedule_data = validated_data.pop('schedule', None)
        

        # Validate requested columns exist in the sheet
        df = pd.read_excel(validated_data['file'], sheet_name=validated_data['sheet_name'])
        available_columns = df.columns.tolist()
        print('available columns in sheet:', available_columns)
        column_names = [col['name'] for col in columns]
        print("column names from request:", column_names)
        if not all(col in available_columns for col in column_names):
            raise Exception("Some requested columns do not exist in the sheet")
        

        # Create Excel upload
        excel_upload = ExcelUpload.objects.create(
            **validated_data, 
            table_name=f"{validated_data['file'].name.split('.')[0].lower()}_{validated_data['sheet_name'].lower()}"
        )
        
        # Create columns
        for column in columns:
            Column.objects.create(excel_upload=excel_upload, **column)
        
        # Create schedule if provided
        schedule = None
        if schedule_data:
            schedule = Schedule.objects.create(
                excel_upload=excel_upload, 
                scheduled_at=schedule_data
            )

            trigger_schedule.apply_async(
                args=[schedule.id],
                eta=schedule.scheduled_at
            )
        
        return schedule