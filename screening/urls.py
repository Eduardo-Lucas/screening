from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobDescriptionViewSet, ResumeViewSet, CandidateRankViewSet

router = DefaultRouter()
router.register('job-descriptions', JobDescriptionViewSet)
router.register('resumes', ResumeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rank-candidates/', CandidateRankViewSet.as_view({'post': 'create'})),
]
