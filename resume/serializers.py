from rest_framework import serializers
from .models import ResumeAnalysis
class ResumeAnalysisSerializer(serializers.ModelSerializer):
    detected_name = serializers.CharField(required=False, allow_blank=True)
    detected_role = serializers.CharField(required=False, allow_blank=True)
    experience_level = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model=ResumeAnalysis
        fields="__all__"
        extra_kwargs={"resume":{"required":False}}
