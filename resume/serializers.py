from rest_framework import serializers
from .models import ResumeAnalysis
class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResumeAnalysis
        fields="__all__"
        extra_kwargs={"resume":{"required":False},"detected_name":{"required":False},"detected_role":{"required":False},"experience_level":{"required":False},"match_score":{"required":False},"matched_skills":{"required":False},"missing_skills":{"required":False},"suggestions":{"required":False}}
