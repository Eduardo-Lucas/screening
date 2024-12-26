from django.db import models
from django.contrib.auth.models import User

class JobDescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relates to a specific user
    candidate_name = models.CharField(max_length=200)
    uploaded_file = models.FileField(upload_to='resumes/')
    parsed_text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.candidate_name


class CandidateRank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relates to a specific user
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    similarity_score = models.FloatField()

    def __str__(self):
        return f"{self.resume.candidate_name} - {self.similarity_score}"
