from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    USER_TYPE_CHOICES = (
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='candidate')

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"
