from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from .permissions import IsCandidate, IsRecruiter


class RegisterCandidateView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            raise ValidationError('Username, email, and password are required.')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')

        # Create user and assign 'candidate' type
        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.user_type = 'candidate'
        user.save()

        return Response({'message': 'Candidate registered successfully!'}, status=status.HTTP_201_CREATED)


class RegisterRecruiterView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            raise ValidationError('Username, email, and password are required.')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Username already exists.')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')

        # Create user and assign 'recruiter' type
        user = User.objects.create_user(username=username, email=email, password=password)
        user.profile.user_type = 'recruiter'
        user.save()

        return Response({'message': 'Recruiter registered successfully!'}, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            raise ValidationError('Username and password are required.')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    

class CandidateOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsCandidate]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'This is a candidate only endpoint!'}, 
                        status=status.HTTP_200_OK)
    
class RecruiterOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request, *args, **kwargs):
        return Response({'message': 'This is a recruiter only endpoint!'}, 
                        status=status.HTTP_200_OK)


class AllUsersView(APIView):
    def get(self, request, *args, **kwargs):
        # FIXME: Show the user profile data as well
        users = User.objects.prefetch_related('profile').all()
        return Response({'users': users.values()}, status=status.HTTP_200_OK)
