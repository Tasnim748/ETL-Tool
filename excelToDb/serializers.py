from importlib.metadata import requires
from rest_framework import serializers
from excelToDb.models import Column, ExcelUpload, Schedule

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['name']


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['scheduled_at']


class ExcelUploadViewSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer(required=False)
    columns = ColumnSerializer(required=False, many=True)
    class Meta:
        model = ExcelUpload
        fields = ['id', 'file', 'sheet_name', 'columns', 'schedule']


class ExcelUploadCreateSerializer(serializers.ModelSerializer):
    schedule = serializers.DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])
    columns = serializers.CharField(required=False)

    class Meta:
        model = ExcelUpload
        fields = ['id', 'file', 'sheet_name', 'columns', 'schedule']

    def create(self, validated_data):
        columns = validated_data.pop('columns')
        schedule_data = validated_data.pop('schedule', None)
        columns_data = [col.strip() for col in columns.split(',')]
        
        excel_upload = ExcelUpload.objects.create(
            **validated_data, 
            table_name=f"excel_data_{validated_data['sheet_name'].lower()}_{ExcelUpload.objects.count() + 1}"
        )
        
        # Create columns
        for column_data in columns_data:
            Column.objects.create(excel_upload=excel_upload, name=column_data)
        
        # Create schedule if provided
        if schedule_data:
            Schedule.objects.create(
                excel_upload=excel_upload, 
                scheduled_at=schedule_data
            )
        
        return excel_upload