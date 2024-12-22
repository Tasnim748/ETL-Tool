ExcelUploadRequest = {
    'multipart/form-data': {
        'type': 'object',
        'properties': {
            'file': {
                'type': 'string',
                'format': 'binary'
            },
            'columns': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'type': {'type': 'string'}
                    }
                }
            },
            'sheet_name': {
                'type': 'string'
            },
            'schedule': {
                'type': 'string',
                'format': 'date-time',
                'example': '2024-12-22T17:52'
            }
        },
        'required': ['file']
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