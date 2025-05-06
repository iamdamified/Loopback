from rest_framework import serializers
from .models import Weeklycheckin


# WEEKLY CHECKINS SERIALIZERS
class WeeklycheckinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weeklycheckin
        fields = '__all__'
        read_only_fields = ['created_by', 'created']