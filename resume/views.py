# from .ai import analyze_resume
# from .models import Resume
# from .serializers import ResumeAnalysisSerializer
# import json
# from rest_framework import status
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .utils import extract_text

# @method_decorator(csrf_exempt, name="dispatch")
# class ResumeUploadAPI(APIView):
#     def post(self,request):
#         resume_file=request.FILES.get("resume")
#         resume=Resume.objects.create(file=resume_file)
#         file_path=resume.file.path
#         resume_text=extract_text(file_path)
#         return Response({
#             "resume_id":resume.id,
#             "resume_text":resume_text})

# class ResumeAnalyzeAPI(APIView):
#     def post(self,request):
#         resume_id=request.data.get('resume_id')
#         resume=Resume.objects.get(id=resume_id)
#         text=extract_text(resume.file.path)
#         # print(f'PDF TEXT{text}')
#         result=analyze_resume(text)
#         print(f'LLL Data{result}')
#         if not result:
#             return Response({"Error":"Not LLM Data"},status=500)
        
#         serializer=ResumeAnalysisSerializer(data=result)
        
#         serializer.is_valid(raise_exception=True)
#         print(f'Final Data{serializer.validated_data}')
#         obj=serializer.save(resume=resume)
#         return Response(ResumeAnalysisSerializer(obj).data)

from .ai import analyze_resume
from .models import Resume
from .serializers import ResumeAnalysisSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .utils import extract_text


# @method_decorator(csrf_exempt, name="dispatch")
# class ResumeUploadAPI(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request):
#         # return Response({"ok": True})
#         resume_file = request.FILES.get("resume")
#         if not resume_file:
#             return Response({"error": "No resume file"}, status=400)

#         resume = Resume.objects.create(file=resume_file)

#         resume_text = extract_text(resume.file.path)
#         if not resume_text:
#             return Response(
#                 {"error": "Unreadable or scanned PDF"},
#                 status=400
#             )

#         return Response({
#             "resume_id": resume.id,
#             "resume_text": resume_text
#         })

@method_decorator(csrf_exempt, name="dispatch")
class ResumeUploadAPI(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        resume_file = request.FILES.get("resume")

        if not resume_file:
            return Response(
                {"error": "No resume file received"},
                status=400
            )

        resume = Resume.objects.create(file=resume_file)

        try:
            resume_text = extract_text(resume.file.path)
        except Exception as e:
            print("Extract error:", e)
            return Response(
                {"error": "Failed to read resume"},
                status=400
            )

        return Response({
            "resume_id": resume.id,
            "resume_text": resume_text
        })

   
        


@method_decorator(csrf_exempt, name="dispatch")
class ResumeAnalyzeAPI(APIView):

    def post(self, request):
        resume_id = request.data.get("resume_id")
        if not resume_id:
            return Response({"error": "resume_id missing"}, status=400)

        try:
            resume = Resume.objects.get(id=resume_id)
        except Resume.DoesNotExist:
            return Response({"error": "Invalid resume_id"}, status=404)

        text = extract_text(resume.file.path)
        if not text:
            return Response({"error": "Resume text empty"}, status=400)

        result = analyze_resume(text)
        if not result:
            return Response({"error": "Gemini returned no data"}, status=500)

        serializer = ResumeAnalysisSerializer(data=result)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(resume=resume)

        return Response(ResumeAnalysisSerializer(obj).data)
