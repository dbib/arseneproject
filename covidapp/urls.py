# ajout des urls de notre application
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('manager_dashboard/<int:manager_id>/', views.manager_dashboard, name='manager_dashboard'),
    path('add_hospital/', views.add_hospital, name='add_hospital'),
    # Add other URLs as needed
]
