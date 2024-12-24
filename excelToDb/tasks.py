from celery import shared_task
from datetime import datetime, timezone

from excelToDb.models import Schedule
from excelToDb.utils.runSchedule import run_schedule
# from excelToDb.models import Schedule
# from excelToDb.utils.runSchedule import run_schedule  # Import the core logic

# @shared_task
# def execute_schedule(schedule_id):
#     """
#     Execute a specific schedule by its ID.
#     """
#     try:
#         schedule = Schedule.objects.select_related('excel_upload').get(id=schedule_id)
#         if datetime.now(timezone.utc) < schedule.scheduled_at:
#             return f"Schedule {schedule_id} is not ready to execute."
#         result = run_schedule(schedule)
#         return f"Schedule {schedule_id} executed successfully: {result}"
#     except Schedule.DoesNotExist:
#         return f"Schedule with ID {schedule_id} does not exist."
#     except Exception as e:
#         return f"Error executing schedule {schedule_id}: {e}"

@shared_task
def trigger_schedule(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    print(schedule.scheduled_at)
    print(f"Schedule trigger: Task executed for schedule {schedule_id} at {datetime.now()}")
    run_schedule(schedule)
