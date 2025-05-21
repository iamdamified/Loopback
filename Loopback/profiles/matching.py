from .models import MentorProfile, MenteeProfile


def get_suggested_mentors_for_mentee(mentee_profile):
    mentors = MentorProfile.objects.all()
    suggestions = []

    for mentor in mentors:
        score = 0
        if mentor.goals and mentee_profile.goals:
            common_goals = set(mentor.goals.lower().split()) & set(mentee_profile.goals.lower().split())
            score += len(common_goals)

        if mentor.interests and mentee_profile.interests:
            common_interests = set(mentor.interests.lower().split()) & set(mentee_profile.interests.lower().split())
            score += len(common_interests)

        suggestions.append((mentor, score))

    suggestions.sort(key=lambda x: x[1], reverse=True)
    return [mentor for mentor, _ in suggestions if _ > 0]  # only return non-zero matches

