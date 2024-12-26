from django.urls import path
from .views import RegisterCandidateView, RegisterRecruiterView, LoginUserView, AllUsersView

urlpatterns = [
    path('register_candidate/', RegisterCandidateView.as_view(), name='register_candidate'),
    path('register_recruiter/', RegisterRecruiterView.as_view(), name='register_recruiter'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('get_all_users/', AllUsersView.as_view(), name='get_all_users'),
]
