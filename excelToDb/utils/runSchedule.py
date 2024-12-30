from csv import excel
import numpy as np
import pandas as pd
from django.db import connection
from django.utils.timezone import now
from excelToDb.models import Schedule
from excelToDb.utils.SQLServerConnection import SQLServerConnection

def run_schedule(schedule: Schedule):
    excel_upload = schedule.excel_upload

    databaseinfo=None
    try:
        databaseinfo = excel_upload.databaseinfo
    except Exception as e:
        print(e)
        return

    # databaseinfo attributes
    server_ip = databaseinfo.server_ip
    database_name = databaseinfo.database_name
    table_name = databaseinfo.table_name
    user_id = databaseinfo.user_id
    password = databaseinfo.password

    sheet_name = excel_upload.sheet_name
    scheduled_at = schedule.scheduled_at

    # Ensure the schedule is not executed before the scheduled time
    if now() < scheduled_at:  # Use Django's timezone-aware now()
        return f"Schedule for {table_name} is not ready to execute."

    # Generate table creation query
    columns = excel_upload.columns.all()  # Fetch related Column objects
    columns_definition = ", ".join([
        f"[{col.name}] {col.type if col.type in ['INT', 'FLOAT', 'NVARCHAR(MAX)', 'TEXT'] else 'TEXT'}"
        for col in columns
    ])

    # Load data from the Excel file
    excel_file_path = excel_upload.file.path
    try:
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        df = df.replace({np.nan: ''})
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Filter data based on selected columns
    selected_columns = [col.name for col in columns]
    filtered_data = df[selected_columns]

    try:
        with SQLServerConnection(server_ip, database_name, user_id, password) as sql_conn:
            # Create table if it doesn't exist
            sql_conn.create_table_if_not_exists(table_name, columns_definition)
            # Your existing code for data insertion goes here
            cursor = sql_conn.connection.cursor()
            
            
            # Insert data into the table
            try:
                with sql_conn.connection.cursor() as cursor:
                    for _, row in filtered_data.iterrows():
                        placeholders = ", ".join(["?"] * len(selected_columns))
                        insert_query = f"INSERT INTO {table_name} ({', '.join(selected_columns)}) VALUES ({placeholders})"
                        cursor.execute(insert_query, tuple(row))
                        sql_conn.connection.commit()
            except Exception as e:
                print(f"Error on inserting data: {e}")
                return


    except Exception as e:
        print(f"Error with database: {e}")
        return


    # Mark the schedule as executed
    schedule.is_executed = True
    schedule.save()

    message = f"Schedule for {table_name} executed successfully."
    print(message)
    return message
