from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import JobDescription, Resume, CandidateRank
from .serializers import JobDescriptionSerializer, ResumeSerializer
from .utils import extract_resume_text, calculate_similarity

class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

    def create(self, request, *args, **kwargs):
        # Save the uploaded file
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            resume = serializer.save()
            resume_path = resume.uploaded_file.path
            
            # Extract text and save it
            parsed_text = extract_resume_text(resume_path)
            resume.parsed_text = parsed_text
            resume.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CandidateRankViewSet(viewsets.ViewSet):
    def create(self, request):
        job_id = request.data.get('job_id')
        resumes = Resume.objects.all()
        job = JobDescription.objects.get(id=job_id)

        resume_texts = [resume.parsed_text for resume in resumes]
        scores = calculate_similarity(job.description, resume_texts)

        for i, resume in enumerate(resumes):
            CandidateRank.objects.update_or_create(
                resume=resume,
                job_description=job,
                defaults={'similarity_score': scores[i]}
            )
        return Response({"message": "Ranking complete!"})
