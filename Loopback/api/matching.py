from profiles.models import Profile
from mentorship.models import Mentorship
from django.utils import timezone
from django.db.models import Count



# def search_mentor_for_mentee(mentee_profile):
#     mentors = Profile.objects.filter(role='mentor')
#     best_match = None
#     best_score = -1

#     for mentor in mentors:
#         # Calculate simple match score
#         interest_overlap = mentee_profile.interests.filter(id__in=mentor.interests.values_list('id', flat=True)).count()
#         skill_overlap = mentee_profile.skills.filter(id__in=mentor.skills.values_list('id', flat=True)).count()

#         score = interest_overlap * 2 + skill_overlap  # Weigh interests higher

#         if score > best_score:
#             best_match = mentor
#             best_score = score

#     return best_match


def search_mentor_for_mentee(mentee_profile):
    mentors = Profile.objects.filter(role='mentor')
    best_match = None
    best_score = 0

    for mentor in mentors:
        # Skip mentors already matched in a loop
        if Mentorship.objects.filter(mentor=mentor, is_active=True).exists():
            continue

        # Score: overlap of interests and skills
        interest_overlap = len(set(mentee_profile.interests.all()) & set(mentor.interests.all()))
        skill_overlap = len(set(mentee_profile.skills.all()) & set(mentor.skills.all()))
        score = interest_overlap + skill_overlap

        if score > best_score:
            best_score = score
            best_match = mentor

    return best_match

def match_pending_mentees():
    mentees = Profile.objects.filter(role='mentee')
    today = timezone.now().date()

    for mentee in mentees:
        # Skip if already in an active loop
        if Mentorship.objects.filter(mentee=mentee.user, status='active').exists():
            continue

        mentor_profile = search_mentor_for_mentee(mentee)

        if mentor_profile:
            Mentorship.objects.create(
                mentor=mentor_profile.user,
                mentee=mentee.user,
                start_date=today,
                end_date=today + timezone.timedelta(weeks=4),
                status='active'
            )