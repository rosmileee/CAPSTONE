from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('eye_screening', 'Eye Screening'),
        ('consultation', 'Consultation'),
        # Add more services if needed
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.CharField(max_length=20)  # To store selected time
    doctor_name = models.CharField(max_length=100)
    
    # New fields from frontend
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    reason = models.TextField()
    booking_for = models.CharField(max_length=20)  # 'yourself' or 'someone_else'
    
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.service_type} on {self.appointment_date}"
