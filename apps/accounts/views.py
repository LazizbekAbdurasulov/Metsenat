from .serializers import UniversitySerializer, SponsorSerializer, StudentSerializer, SponsorshipSerializer
from .models import Sponsorship, Student, Universities, Sponsor
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

class UniversityViewSet(ModelViewSet):
    queryset = Universities.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UniversitySerializer

class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = SponsorSerializer

class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = StudentSerializer

class SponsorshipViewSet(ModelViewSet):
    queryset = Sponsorship.objects.all()
    permission_classes =[
        permissions.AllowAny
    ]
    serializer_class = SponsorshipSerializer