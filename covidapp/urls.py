# ajout des urls de notre application
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('manager_login/', views.manager_login, name='manager_login'),
    path('manager_dashboard/<int:manager_id>/', views.manager_dashboard, name='manager_dashboard'),
    path('add_hospital/', views.add_hospital, name='add_hospital'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('doctor_login/', views.doctor_login, name='doctor_login'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor_signout/', views.doctor_signout, name='doctor_signout'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('user_registration/', views.user_registration, name='user_registration'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('ask_consultation/', views.ask_consultation, name='ask_consultation'),
    # Add other URLs as needed
]
