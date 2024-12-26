import datetime


ExcelUploadRequest = {
    'multipart/form-data': {
        'type': 'object',
        'properties': {
            'file': {
                'type': 'string',
                'format': 'binary',
                'description': 'File name must be without any space'
            },
            'columns': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'type': {'type': 'string'}
                    }
                },
                'description': "Column type should be from ['INT', 'FLOAT', 'NVARCHAR(MAX)', 'TEXT']"
            },
            'sheet_name': {
                'type': 'string',
                'description': 'Sheet name cannot contain any space'
            },
            'schedule': {
                'type': 'string',
                'format': 'date-time',
                'example': datetime.datetime.now() + datetime.timedelta(minutes=15)
            }
        },
        'required': ['file', 'columns', 'sheet_name']
    }
}


ExcelUploadResponse = {
    201: {
        'type': 'object',
        'properties': {
            'message': {
                'example': 'File uploaded successfully'
            }
        }
    }
}


SetSchedule = {
    'application/json': {
        'type': 'object',
        'properties': {
            'excelUploadId': {
                'type': 'integer',
                'description': 'The id of your excel upload record'
            },
            'schedule_time': {
                'type': 'string',
                'format': 'date-time',
                'example': datetime.datetime.now() + datetime.timedelta(minutes=15)
            }
        }
    }
}