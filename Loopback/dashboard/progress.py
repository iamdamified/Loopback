from rest_framework import serializers

class ProgressEventSerializer(serializers.Serializer):
    type = serializers.CharField()
    date = serializers.DateTimeField()
    week_number = serializers.IntegerField(required=False)
    weekly_goals = serializers.CharField(required=False)
    progress = serializers.CharField(required=False)
    challenges = serializers.CharField(required=False)
    feedback = serializers.CharField(required=False)
    status = serializers.CharField(required=False)

class ProgressHistorySerializer(serializers.Serializer):
    loop = serializers.DictField()
    progress_timeline = ProgressEventSerializer(many=True)





from rest_framework.views import APIView
from rest_framework.response import Response
from mentorship.models import MentorshipLoop
from matchrequest.models import MeetingSchedule
from weeklycheckin.models import WeeklyCheckIn

class ProgressHistoryView(APIView):
    def get(self, request, loop_id):
        # Get loop
        loop = MentorshipLoop.objects.get(id=loop_id)
        # Gather meetings
        meetings = MeetingSchedule.objects.filter(match_request__mentor=loop.mentor, match_request__mentee=loop.mentee)
        # Gather checkins
        checkins = WeeklyCheckIn.objects.filter(loop=loop)
        # Compose timeline
        events = []
        for m in meetings:
            events.append({
                "type": "meeting",
                "date": m.scheduled_time,
                "weekly_goals": m.weekly_goals,
            })
        for c in checkins:
            events.append({
                "type": "checkin",
                "date": c.checkin_date,
                "week_number": c.week_number,
                "progress": c.progress,
                "challenges": c.challenges,
                "feedback": c.feedback,
                "status": c.status,
            })
        # Sort by date
        events.sort(key=lambda x: x['date'])
        data = {
            "loop": {
                "status": loop.status,
                "start_date": loop.start_date,
                "end_date": loop.end_date,
                "goals": loop.purpose,
            },
            "progress_timeline": events
        }
        return Response(data)