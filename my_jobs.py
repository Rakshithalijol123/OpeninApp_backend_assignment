import schedule
import time

from .my_tasks import get_users_to_call, update_priority, get_tasks, get_users

tasks_collection = "Test_task"
users_collection = "Test_user"

cron_interval_minutes = 1440


def cron_get_users_to_call():
    print("Executing get_users_to_call cron job...")
    tasks = get_tasks()
    users = get_users()
    get_users_to_call(tasks, users)


def cron_update_priority(task_id: int, due_date):
    print("Executing update_priority cron job...")
    update_priority(task_id, due_date)


schedule.every(cron_interval_minutes).minutes.do(cron_get_users_to_call)
schedule.every(cron_interval_minutes).minutes.do(cron_update_priority)

while True:
    schedule.run_pending()
    time.sleep(1)
