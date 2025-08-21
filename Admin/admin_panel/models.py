from django.db import models
from django.contrib.auth.models import User

# Make sure you have these models defined or adapt them as needed
# For simplicity, I'm assuming Doctor and Appointment models exist.
# You will need to add the new DoctorAvailability model below.

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"


class Appointment(models.Model):
    # This model acts as both an appointment and a patient record
    patient_first_name = models.CharField(max_length=100)
    patient_last_name = models.CharField(max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_datetime = models.DateTimeField()
    status = models.CharField(max_length=50, default='Scheduled') # E.g., 'Scheduled', 'Completed', 'Canceled'
    archive = models.BooleanField(default=False)
    # Add other fields like patient_notes, diagnosis, etc.

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.last_name} for {self.patient_first_name} {self.patient_last_name}"


# NEW MODEL: DoctorAvailability to store doctor's time slots
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    # Storing time slots as JSONField, which is a list of dictionaries
    # Example: [{'start': '09:00', 'end': '09:30'}, {'start': '10:00', 'end': '10:30'}]
    time_slots = models.JSONField(default=list)

    class Meta:
        unique_together = ('doctor', 'date') # Ensure one availability record per doctor per day

    def __str__(self):
        return f"Availability for Dr. {self.doctor.user.last_name} on {self.date}"
