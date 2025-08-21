from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse # Import JsonResponse and HttpResponse
from .models import Doctor, Appointment # Import your new models
from django.views.decorators.http import require_POST
import datetime # Import the datetime module

# --- Existing Views ---

@login_required
def admin_home(request):
    # Fetch real data for the dashboard
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='Scheduled').count()
    active_doctors = Doctor.objects.count()

    context = {
        'total_appointments': total_appointments,
        'pending_appointments': pending_appointments,
        'active_doctors': active_doctors,
    }
    return render(request, 'admin_panel/home.html', context)

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('admin_home')
            else:
                error = 'Invalid credentials. Please try again.'
                return render(request, 'admin_panel/login.html', {'error': error})
        except User.DoesNotExist:
            error = 'User with this email does not exist.'
            return render(request, 'admin_panel/login.html', {'error': error})
        except Exception as e:
            error = 'An error occurred: ' + str(e)
            return render(request, 'admin_panel/login.html', {'error': error})
    
    return render(request, 'admin_panel/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def admin_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            error = 'Email is already registered.'
            return render(request, 'admin_panel/register.html', {'error': error})

        # Check if username is already in use (Django handles this automatically, but good to be explicit)
        if User.objects.filter(username=username).exists():
            error = 'Username is already taken.'
            return render(request, 'admin_panel/register.html', {'error': error})

        # Create the new user
        user = User.objects.create_user(username=username, email=email, password=password)
        # You can also create a related Doctor object here if needed
        # Doctor.objects.create(user=user, specialty="General Practitioner") 
        
        return redirect('admin_login')
    
    return render(request, 'admin_panel/register.html')

@login_required
def monitor_appointments(request):
    appointments = Appointment.objects.filter(archive=False).order_by('-appointment_datetime')
    return render(request, 'admin_panel/appointments.html', {'appointments': appointments})

@login_required
@require_POST
def archive_appointment(request):
    appointment_id = request.POST.get('id')
    try:
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        appointment.archive = True
        appointment.save()
        return JsonResponse({'success': True, 'message': 'Appointment archived successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def admin_profile(request):
    return render(request, 'admin_panel/profile.html', {'user': request.user})

@login_required
def manage_doctors_availability(request):
    doctors = Doctor.objects.all()
    # You will need to implement logic to get actual occupied and vacant slots
    # For now, this is a placeholder
    for doctor in doctors:
        doctor.occupied_slots = ['9:00 AM', '9:30 AM'] # Dummy data
        doctor.vacant_slots = ['10:00 AM', '10:30 AM'] # Dummy data
    
    context = {'doctors': doctors}
    return render(request, 'admin_panel/manage_doctors_availability.html', context)

@login_required
@require_POST
def set_doctor_availability(request):
    doctor_id = request.POST.get('doctor_id')
    date_str = request.POST.get('date')
    start_time_str = request.POST.get('start_time')
    end_time_str = request.POST.get('end_time')

    if not all([doctor_id, date_str, start_time_str, end_time_str]):
        return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

    try:
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        # Here, you would save this new availability to your database.
        # This requires a new model for doctor schedules, e.g., DoctorSchedule.
        # For now, we'll just return a success message.
        print(f"Saving availability for {doctor.user.username} on {date_str} from {start_time_str} to {end_time_str}")
        return JsonResponse({'success': True, 'message': 'Availability saved successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def doctor_overview_patients_record(request):
    # This view now only shows non-archived patient records
    patients = Appointment.objects.filter(archive=False).order_by('patient_last_name')
    context = {'patients': patients}
    return render(request, 'admin_panel/doctor_overview_patients_record.html', context)

@login_required
@require_POST
def archive_patient(request):
    patient_id = request.POST.get('id')
    try:
        patient_record = get_object_or_404(Appointment, pk=patient_id)
        patient_record.archive = True
        patient_record.save()
        return JsonResponse({'success': True, 'message': 'Patient record archived successfully.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@login_required
def add_appointment(request):
    if request.method == 'POST':
        # Makuha ang data gikan sa form
        patient_first_name = request.POST.get('patient_first_name')
        patient_last_name = request.POST.get('patient_last_name')
        patient_age = request.POST.get('patient_age')
        appointment_datetime_str = request.POST.get('appointment_datetime')
        severity = request.POST.get('severity')
        status = request.POST.get('status')
        doctor_id = request.POST.get('doctor_id')

        try:
            # I-convert ang string sa datetime object
            appointment_datetime = datetime.datetime.fromisoformat(appointment_datetime_str)

            # Kuhaon ang Doctor object
            doctor = get_object_or_404(Doctor, pk=doctor_id)

            # Maghimo og bag-ong appointment object
            new_appointment = Appointment(
                patient_first_name=patient_first_name,
                patient_last_name=patient_last_name,
                patient_age=patient_age,
                appointment_datetime=appointment_datetime,
                severity=severity,
                status=status,
                doctor_id=doctor
            )
            
            # I-save ang bag-ong appointment sa database
            new_appointment.save()

            # I-redirect ang user sa appointments page
            return redirect('monitor_appointments')

        except Exception as e:
            # Kung dunay error, i-display ang error message
            error = f'An error occurred: {e}'
            return render(request, 'admin_panel/add_appointment.html', {'error': error})
    
    # I-render ang form para sa pag-add og appointment
    doctors = Doctor.objects.all()
    return render(request, 'admin_panel/add_appointment.html', {'doctors': doctors})
