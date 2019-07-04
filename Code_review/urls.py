"""Garmin_1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import include, path
from app_search import views as search_views
from app_config import views as config_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', search_views.search, name='app_search'),
    path('config/', config_views.config, name='app_config'),
    path('populate/', search_views.populate, name='populate'),
    path('table/', search_views.api, name='table'),
    path('view/', search_views.lineNums, name='view_file')
]
