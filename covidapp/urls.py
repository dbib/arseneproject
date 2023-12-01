# ajout des urls de notre application
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('manager_dashboard/<int:manager_id>/', views.manager_dashboard, name='manager_dashboard'),
    path('add_hospital/', views.add_hospital, name='add_hospital'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_signout/', views.doctor_signout, name='doctor_signout'),
    path('add_patient/', views.add_patient, name='add_patient'),
    # Add other URLs as needed
]
