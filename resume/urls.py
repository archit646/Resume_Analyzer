from django.urls import path

from .views import ResumeAnalyzeAPI, ResumeUploadAPI
urlpatterns = [
    path("upload/",ResumeUploadAPI.as_view()),
    path("analyze/",ResumeAnalyzeAPI.as_view())
]