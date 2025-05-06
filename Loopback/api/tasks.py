from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from mentorship.models import Mentorship
from users.models import User
from django.contrib.auth import get_user_model
from .matching import match_pending_mentees


User = get_user_model()

@shared_task
def weekly_checkin_reminder():
    today = timezone.now().date()
    loops = Mentorship.objects.filter(status='ongoing', start_date__lte=today, finish_date__gte=today)

    for loop in loops:
        week_number = ((today - loop.start_date).days // 7) + 1
        # Only send on the start of each week
        if (today - loop.start_date).days % 7 == 0:
            subject = f"Weekly Check-in Reminder (Week {week_number}) - Loop {loop.id}"
            message = (
                f"Hello {loop.mentee.username} & {loop.mentor.username},\n\n"
                f"This is your Week {week_number} check-in reminder.\n"
                "Please remember to check in with each other.\n\n"
                "Thanks,\nThe Loopback Team"
            )
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [loop.mentor.email, loop.mentee.email])




@shared_task
def loop_feedback_reminder():
    today = timezone.now().date()
    loops = Mentorship.objects.filter(status='ongoing', finish_date__lt=today)

    for loop in loops:
        loop.status = 'completed'
        loop.save()

        subject = f"Loopback Feedback Reminder - Loop {loop.id}"
        message = (
            f"Hi {loop.mentee.username} & {loop.mentor.username},\n\n"
            "Your mentorship loop has ended. We'd love your feedback to help us improve!\n"
            "Please log in to provide your feedback.\n\n"
            "Thanks,\nThe Loopback Team"
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [loop.mentor.email, loop.mentee.email])



@shared_task
def run_auto_matching():
    match_pending_mentees()

