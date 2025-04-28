from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from users.models import Mentorship, User
from django.contrib.auth import get_user_model
from .matching import match_pending_mentees


User = get_user_model()

@shared_task
def weekly_checkin_reminder():
    today = timezone.now().date()
    loops = Mentorship.objects.filter(status='ongoing', start_date__lte=today, finish_date__gte=today)

    for loop in loops:
        subject = "Weekly Check-in Reminder from Loopback for" + loop.id
        message = f"Hello {loop.mentee.username} & {loop.mentor.username}, \n\n This is a reminder for your weekly check-in {(today - loop.start_date).days // 7 + 1}.\n Please complete your check-in for this week.\n\n Thank you!"
        send_mail(subject, message, 'no-reply@lookback.com', [loop.mentor.email, loop.mentee.email], fail_silently=False)


@shared_task
def loop_feedback_reminder():
    today = timezone.now().date()
    loops = Mentorship.objects.filter(status='ongoing', finish_date__lt=today)

    for loop in loops:
        loop.status = 'completed'
        loop.save()

        subject = "Loopback Feedback Reminder for Completed Loop" + loop.id
        message = "Hello " + loop.mentee.username + " & " + loop.mentor.username + ", \n\n Your mentorship loop has been completed. Please provide your feedback on Loopback.\n\n Thank you!"
        send_mail(subject, message, 'no-reply@lookback.com', [loop.mentor.email, loop.mentee.email], fail_silently=False)





@shared_task
def run_auto_matching():
    match_pending_mentees()