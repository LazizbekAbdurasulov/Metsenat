from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .pagination import CustomPagination
from .serializers import (UniversitySerializer, SponsorSerializer,
                         StudentSerializer, SponsorshipSerializer,
                         DashboardSerializer, StatDashboardSerializer)
from .models import Sponsorship, Student, Universities, Sponsor

class UniversityViewSet(ModelViewSet):
    queryset = Universities.objects.all()
    serializer_class = UniversitySerializer
    permission_classes = [
        permissions.IsAdminUser
    ]
    pagination_class = CustomPagination


class SponsorViewSet(ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [
      permissions.AllowAny
    ]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'company']
    filterset_fields = ['amount', 'status']
    pagination_class = CustomPagination


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [
        permissions.IsAdminUser
    ]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['first_name', 'last_name']
    filterset_fields = ['degree', 'university']
    pagination_class = CustomPagination


class SponsorshipViewSet(ModelViewSet):
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipSerializer
    permission_classes =[
        permissions.IsAdminUser
    ]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['sponsor__full_name', 'sponsor__company', 'student__first_name', 'student__last_name']
    filterset_fields = ['amount']
    pagination_class = CustomPagination

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        sponsor = Sponsor.objects.get(id=instance.sponsor_id)
        sponsor.amount = sponsor.amount + instance.amount
        sponsor.save()
        self.perform_destroy(instance)
        return Response({"msg":"Deleted."}, status=status.HTTP_204_NO_CONTENT)


class DashboardView(APIView):
    permission_classes = [
        permissions.IsAdminUser
    ]
    @staticmethod
    def get(request, *args, **kwargs):
        dashboard_serializer = DashboardSerializer()
        dashboard_stat_serializer = StatDashboardSerializer()
        return Response(data={
            'money': dashboard_serializer.data,
            'graph': dashboard_stat_serializer.data
        })
