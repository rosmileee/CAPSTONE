# core/urls.py

from django.urls import path
from .views import (
    register_user,
    login_user,
    get_user_profile,
    book_appointment,
)

urlpatterns = [
    # 🔐 Authentication
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),

    # 👤 User Profile
    path('profile/', get_user_profile, name='profile'),

    # 📅 Appointment Booking
    path('book-appointment/', book_appointment, name='book_appointment'),
]
