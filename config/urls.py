from django.contrib import admin
from django.urls import path,include
from apps.authentication.views import LoginView, LogoutView
from apps.accounts.views import DashboardView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('auth/login/', LoginView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('api/dashboard', DashboardView.as_view(), name='dashboard')

]
