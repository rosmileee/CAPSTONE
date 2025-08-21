# admin_panel/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Admin Panel Views
    path('', views.admin_login, name='admin_login'),
    path('home/', views.admin_home, name='admin_home'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('register/', views.admin_register, name='admin_register'),
    
    # New views for your menus
    path('appointments/', views.monitor_appointments, name='monitor_appointments'),
    path('profile/', views.admin_profile, name='admin_profile'),
    path('manage-doctors-availability/', views.manage_doctors_availability, name='manage_doctors_availability'),
    path('doctor-overview-patients-record/', views.doctor_overview_patients_record, name='doctor_overview_patients_record'),

    # API Endpoints (The missing URLs)
    path('appointments/archive/', views.archive_appointment, name='archive_appointment'),
    path('patients/archive/', views.archive_patient, name='archive_patient'),
    path('manage-doctors-availability/set-availability/', views.set_doctor_availability, name='set_doctor_availability'),
]