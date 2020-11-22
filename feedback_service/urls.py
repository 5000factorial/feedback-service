"""feedback_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.root, name='root'),

    path('pool/<int:pk>/', views.PoolView.as_view(), name='pool'),
    
    path('teams/settings/auth/', views.teams_settings_auth, name='teams_settings_auth'),
    path('teams/settings/pool/', views.teams_settings_pool, name='teams_settings_pool'),
    path('teams/settings/save/', views.teams_settings_save, name='teams_settings_auth'),
    
    path('report_builder/', include('report_builder.urls'))
]
