import os

from celery import Celery
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Loopback.settings')

app = Celery('Loopback')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# app.conf.beat_schedule = {
#     'weekly-checkin-reminder': {
#         'task': 'mentorship.tasks.weekly_checkin_reminder',
#         'schedule': crontab(minute=0, hour=8, day_of_week='saturday'),  # Every SATURDAY 8AM
#     },
#     'loop-feedback-reminder': {
#         'task': 'mentorship.tasks.loop_feedback_reminder',
#         'schedule': crontab(minute=0, hour=9, day_of_week='sunday'),  # Every SUNDAY 9AM
#     },
# }



# app.conf.beat_schedule.update({
#     'run-auto-matching-every-day': {
#         'task': 'mentorship.tasks.run_auto_matching',
#         'schedule': crontab(minute=0, hour=1),  # Every day at 1AM
#     },
# })