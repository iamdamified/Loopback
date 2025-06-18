from rest_framework import serializers

class ProgressEventSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["meeting", "checkin"])
    date = serializers.DateTimeField()
    week_number = serializers.IntegerField(required=False)
    weekly_goals = serializers.CharField(required=False)
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    status = serializers.CharField(required=False)

class ProgressHistorySerializer(serializers.Serializer):
    loop = serializers.DictField()
    progress_timeline = ProgressEventSerializer(many=True)




from rest_framework.views import APIView
from rest_framework.response import Response
from mentorship.models import MentorshipLoop
from weeklycheckin.models import WeeklyCheckIn
from rest_framework import status
from django.shortcuts import get_object_or_404

class ProgressHistoryView(APIView):
    def get(self, request, loop_id):
        loop = get_object_or_404(MentorshipLoop, id=loop_id)

        # Events timeline
        events = []

        # Add meeting events
        meetings = WeeklyCheckIn.objects.filter(
            match__mentor=loop.mentor, match__mentee=loop.mentee
        )
        for m in meetings:
            events.append({
                "type": "meeting",
                "date": m.scheduled_date,
                "start_time": m.start_time,
                "weekly_goals": m.weekly_goals,
                "status": m.status,
            })

        # Add check-in events
        checkins = WeeklyCheckIn.objects.filter(loop=loop)
        for c in checkins:
            events.append({
                "type": "checkin",
                "date": c.scheduled_date,
                "week_number": c.week_number,
                "start_time": c.start_time,
                "end_time": c.end_time,
                "status": c.status,
                "weekly_goals": c.weekly_goals,
            })

        # Sort chronologically
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

        serializer = ProgressHistorySerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
