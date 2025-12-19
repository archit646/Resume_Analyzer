from .ai import analyze_resume
from .models import Resume
from .serializers import ResumeAnalysisSerializer
import json
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import extract_text
class ResumeUploadAPI(APIView):
    def post(self,request):
        resume_file=request.FILES.get("resume")
        resume=Resume.objects.create(file=resume_file)
        file_path=resume.file.path
        resume_text=extract_text(file_path)
        return Response({
            "resume_id":resume.id,
            "resume_text":resume_text})

class ResumeAnalyzeAPI(APIView):
    def post(self,request):
        resume_id=request.data.get('resume_id')
        resume=Resume.objects.get(id=resume_id)
        text=extract_text(resume.file.path)
        # print(f'PDF TEXT{text}')
        result=analyze_resume(text)
        print(f'LLL Data{result}')
        if not result:
            return Response({"Error":"Not LLM Data"},status=500)
        
        serializer=ResumeAnalysisSerializer(data=result)
        
        serializer.is_valid(raise_exception=True)
        print(f'Final Data{serializer.validated_data}')
        obj=serializer.save(resume=resume)
        return Response(ResumeAnalysisSerializer(obj).data)
