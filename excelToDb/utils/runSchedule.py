import numpy as np
import pandas as pd
from django.db import connection
from django.utils.timezone import now
from excelToDb.models import Schedule

def run_schedule(schedule: Schedule):
    """
    Executes the schedule for a given Schedule object.

    Args:
        schedule (Schedule): The Schedule object to process.

    Returns:
        str: Summary of the schedule execution.
    """
    excel_upload = schedule.excel_upload
    table_name = excel_upload.table_name
    scheduled_at = schedule.scheduled_at
    sheet_name = excel_upload.sheet_name

    # 1. Ensure the schedule is not executed before the scheduled time
    if now() < scheduled_at:  # Use Django's timezone-aware now()
        return f"Schedule for {table_name} is not ready to execute."

    # 2. Create the table if it does not exist
    columns = excel_upload.columns.all()  # Fetch related Column objects
    column_definitions = ", ".join([
        f"[{col.name}] {col.type if col.type in ['INT', 'FLOAT', 'NVARCHAR(MAX)', 'TEXT'] else 'TEXT'}"
        for col in columns
    ])

    create_table_query = f"""
    IF NOT EXISTS (
        SELECT 1
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_NAME = '{table_name}'
    )
    BEGIN
        CREATE TABLE {table_name} (
            id INT IDENTITY(1,1) PRIMARY KEY,
            {column_definitions}
        );
    END;
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)
    except Exception as e:
        print(f"Error on creating table: {e}")
        return

    # 3. Load data from the Excel file
    excel_file_path = excel_upload.file.path
    try:
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        df = df.replace({np.nan: ''})
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # 4. Filter data based on selected columns
    selected_columns = [col.name for col in columns]
    filtered_data = df[selected_columns]

    # 5. Insert data into the table
    try:
        with connection.cursor() as cursor:
            for _, row in filtered_data.iterrows():
                placeholders = ", ".join(["%s"] * len(selected_columns))
                # print("placeholders:", placeholders)
                insert_query = f"INSERT INTO {table_name} ({', '.join(selected_columns)}) VALUES ({placeholders})"
                # print("insert_query:", insert_query)
                # print("row:", row)
                cursor.execute(insert_query, tuple(row))
    except Exception as e:
        print(f"Error on inserting data: {e}")
        return

    # Mark the schedule as executed
    schedule.is_executed = True
    schedule.save()

    message = f"Schedule for {table_name} executed successfully."
    print(message)
    return message
