
from users.models import User
from .models import Profile, Interest, Skill
from rest_framework import serializers



class ProfileSerializer(serializers.ModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Interest.objects.all()
    )
    skills = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Skill.objects.all()
    )

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'role', 'goals', 'interests', 'skills',
        ]
        read_only_fields = ['user']

    def create(self, validated_data):
        interests = validated_data.pop('interests', [])
        skills = validated_data.pop('skills', [])
        profile = Profile.objects.create(**validated_data)

        profile.interests.set(interests)
        profile.skills.set(skills)
        return profile

    def update(self, instance, validated_data):
        interests = validated_data.pop('interests', None)
        skills = validated_data.pop('skills', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if interests is not None:
            instance.interests.set(interests)

        if skills is not None:
            instance.skills.set(skills)

        instance.save()
        return instance


# For Backend Dynamic input Only.
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ['id', 'name']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name']