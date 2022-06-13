from django.urls import URLPattern
from rest_framework import routers
from .views import UniversityViewSet, SponsorViewSet, StudentViewSet, SponsorshipViewSet

routers = routers.DefaultRouter()
routers.register('api/universities', UniversityViewSet,'Universities')
routers.register('api/sponsors', SponsorViewSet, 'Sponsor')
routers.register('api/students', StudentViewSet, 'Student')
routers.register('api/Sponsorships', SponsorshipViewSet, 'Sponsorship')
urlpatterns = routers.urls