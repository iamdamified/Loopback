from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from weeklycheckin.models import WeeklyCheckIn
from mentorship.models import MentorshipLoop
from datetime import timedelta
from django.utils import timezone


User = get_user_model()

@shared_task
def send_checkin_reminder_email(checkin_id):
    try:
        checkin = WeeklyCheckIn.objects.get(id=checkin_id)
    except WeeklyCheckIn.DoesNotExist:
        return  # silently ignore if not found

    # Only send if check-in is scheduled for tomorrow and still pending
    if checkin.status == 'pending' and checkin.checkin_date == timezone.now().date() + timedelta(days=1):
        loop = checkin.loop
        mentor = loop.mentor.user
        mentee = loop.mentee.user

        subject = f"⏰ Reminder: Week {checkin.week_number} Check-in Tomorrow"
        message = f"""
Hi {mentor.first_name} and {mentee.first_name},

This is a friendly reminder that your Week {checkin.week_number} check-in is scheduled for tomorrow: {checkin.checkin_date}.

Please log in to complete your reflection and progress updates.

- The Mentorship Team
""".strip()

        recipients = [mentor.email, mentee.email]
        if all(recipients):
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=False,
            )




@shared_task
def send_checkin_completed_email(checkin_id):
    try:
        checkin = WeeklyCheckIn.objects.get(id=checkin_id)
    except WeeklyCheckIn.DoesNotExist:
        return  # Exit silently if check-in doesn't exist

    # Ensure the check-in is actually completed
    if checkin.status != WeeklyCheckIn.STATUS_COMPLETED:
        return

    loop = checkin.loop
    mentor = loop.mentor.user
    mentee = loop.mentee.user

    subject = f"✅ Week {checkin.week_number} Check-in Completed"
    message = f"""
Hi {mentor.first_name} and {mentee.first_name},

Both of you have completed the check-in for Week {checkin.week_number} of your mentorship loop.

Keep up the great work!

📅 Date: {checkin.checkin_date}

- The Mentorship Team
""".strip()

    recipient_list = [mentor.email, mentee.email]
    if all(recipient_list):
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )


    


@shared_task
def send_loop_completion_email(loop_id):
    try:
        loop = MentorshipLoop.objects.get(id=loop_id)
    except MentorshipLoop.DoesNotExist:
        return  # Loop doesn't exist; exit silently

    # Optional: Check if the loop has ended and is still active
    if loop.end_date > timezone.now().date() or not loop.is_active:
        return  # Don't send email prematurely or for inactive loops

    mentor = loop.mentor.user
    mentee = loop.mentee.user

    subject = "🎓 Mentorship Loop Completed"
    message = f"""
Hi {mentor.first_name} and {mentee.first_name},

Congratulations on completing your 4-week mentorship loop!

We invite you both to visit the platform and leave feedback about your experience.

Thank you for participating!

- The Mentorship Team
""".strip()

    recipients = [mentor.email, mentee.email]
    if all(recipients):
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=False,
        )



# Wrapper Tasks

@shared_task
def send_all_checkin_reminders():
    tomorrow = timezone.now().date() + timedelta(days=1)
    checkins = WeeklyCheckIn.objects.filter(checkin_date=tomorrow, status='pending')

    for checkin in checkins:
        send_checkin_reminder_email.delay(checkin.id)


@shared_task
def send_all_loop_completion_emails():
    today = timezone.now().date()
    loops = MentorshipLoop.objects.filter(end_date=today, is_active=True)

    for loop in loops:
        send_loop_completion_email.delay(loop.id)

# User = get_user_model()

# @shared_task
# def weekly_checkin_reminder():
#     today = timezone.now().date()
#     loops = Mentorship.objects.filter(status='ongoing', start_date__lte=today, finish_date__gte=today)

#     for loop in loops:
#         week_number = ((today - loop.start_date).days // 7) + 1
#         # Only send on the start of each week
#         if (today - loop.start_date).days % 7 == 0:
#             subject = f"Weekly Check-in Reminder (Week {week_number}) - Loop {loop.id}"
#             message = (
#                 f"Hello {loop.mentee.email} & {loop.mentor.email},\n\n"
#                 f"This is your Week {week_number} check-in reminder.\n"
#                 "Please remember to check in with each other.\n\n"
#                 "Thanks,\nThe Loopback Team"
#             )
#             send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [loop.mentor.email, loop.mentee.email])




# @shared_task
# def loop_feedback_reminder():
#     today = timezone.now().date()
#     loops = Mentorship.objects.filter(status='ongoing', finish_date__lt=today)

#     for loop in loops:
#         loop.status = 'completed'
#         loop.save()

#         subject = f"Loopback Feedback Reminder - Loop {loop.id}"
#         message = (
#             f"Hi {loop.mentee.email} & {loop.mentor.email},\n\n"
#             "Your mentorship loop has ended. We'd love your feedback to help us improve!\n"
#             "Please log in to provide your feedback.\n\n"
#             "Thanks,\nThe Loopback Team"
#         )
#         send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [loop.mentor.email, loop.mentee.email])



# @shared_task
# def run_auto_matching():
#     match_pending_mentees()

