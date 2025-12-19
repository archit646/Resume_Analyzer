from django.db import models
class Resume(models.Model):
    id=models.AutoField(primary_key=True)
    file=models.FileField(upload_to="resumes/")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.id)+self.file.name

class ResumeAnalysis(models.Model):
    resume=models.ForeignKey(Resume,on_delete=models.CASCADE,related_name="analysis")
    detected_name=models.CharField(max_length=100)
    detected_role=models.CharField(max_length=100)
    experience_level=models.CharField(max_length=100)
    match_score=models.IntegerField()
    matched_skills=models.JSONField()
    missing_skills=models.JSONField()
    suggestions=models.JSONField()
    def __str__(self): 
       return str(self.id)+self.detected_role