from django.urls import path

from app_cmp import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pop/', views.populateDB,name = 'populate'),
    path('files/',views.fileList , name = 'fileList'),
    path('files/displayFile/<str:value>',views.displayFile , name = 'displayFile'),
    path('files/displayFilePlain/<str:value>',views.displayFilePlain , name = 'displayFilePlain'),
]