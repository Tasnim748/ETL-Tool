from celery import shared_task
from datetime import datetime, timezone

from excelToDb.models import Schedule
from excelToDb.utils.runSchedule import run_schedule


@shared_task
def trigger_schedule(schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    print(schedule.scheduled_at)
    print(f"Schedule trigger: Task executed for schedule {schedule_id} at {datetime.now()}")
    run_schedule(schedule)
