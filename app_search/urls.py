from django.urls import path
from . import views

urlpatterns = [
   path('', views.search, name='app_search'),
   path('populate/', views.populate, name='populate'),
   path('table/', views.api, name='table'),
   path('view/<int:doc_id>/', views.view_file, name='view_file'),
   path('view/<int:doc_id>/<str:arguString>/', views.view_file_argu, name='view_file_argu')
]