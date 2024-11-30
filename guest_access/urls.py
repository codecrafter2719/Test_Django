from django.urls import path,include
from . import views

app_name = 'guest_access'

urlpatterns = [
    # path('',views.about,name='about'),
    path('symptom_checker/', views.symptom_checker, name='view_symptoms'),
    path('summary/', views.disease_summary, name='summary'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),

]