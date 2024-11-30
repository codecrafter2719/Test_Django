# user_auth/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    PatientRegistrationForm, DoctorRegistrationForm1, DoctorRegistrationForm2,
    DoctorRegistrationForm3, DoctorRegistrationForm4, DoctorRegistrationForm5
)
from .models import PatientProfile, DoctorProfile, Specialization
# user_auth/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import verify_pmdc_number

# user_auth/views.py

@login_required
def doctor_dashboard(request):
    doctor_profile = request.user.doctorprofile

    # Restrict access for unapproved doctors
    if not doctor_profile.is_approved:
        return render(request, 'user_auth/doctor_dashboard.html', {
            'doctor_profile': doctor_profile,
            'restricted': True,  # Pass a flag to indicate restricted access
        })

    # Render full dashboard for approved doctors
    return render(request, 'user_auth/doctor_dashboard.html', {
        'doctor_profile': doctor_profile,
        'restricted': False,  # Pass a flag to indicate full access
    })

def home(request):
    return render(request, 'user_auth/home.html')

def patient_register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            PatientProfile.objects.create(
                user=user,
                phone_no=form.cleaned_data['phone_no'],
                full_name=form.cleaned_data['full_name']
            )
            messages.success(request, 'Registration successful. Please login.')
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    return render(request, 'user_auth/patient_register.html', {'form': form})

# user_auth/views.py


def doctor_register_step1(request):
    if request.method == 'POST':
        form = DoctorRegistrationForm1(request.POST)
        if form.is_valid():
            user = form.save()
            # Retrieve the verified doctor data
            verified_doctor = form.cleaned_data.get('verified_doctor')

            # Create DoctorProfile with verified data
            DoctorProfile.objects.create(
                user=user,
                phone_no=form.cleaned_data['phone_no'],
                full_name=form.cleaned_data['full_name'],
                pmdc_no=form.cleaned_data['pmdc_no'],
                is_verified=True,  # Automatically set after PMDC API validation
                is_approved=False,  # Requires admin approval
            )

            # Log the user in immediately after registration
            login(request, user)
            return redirect('doctor_register_step2')
    else:
        form = DoctorRegistrationForm1()
    return render(request, 'user_auth/doctor_register_step1.html', {'form': form})

# Doctor Registration Step 1 - Sign up and Log in User
# def doctor_register_step1(request):
#     if request.method == 'POST':
#         form = DoctorRegistrationForm1(request.POST)
#         if form.is_valid():
#             user = form.save()
#             DoctorProfile.objects.create(
#                 user=user,
#                 phone_no=form.cleaned_data['phone_no'],
#                 full_name=form.cleaned_data['full_name'],
#                 pmdc_no=form.cleaned_data['pmdc_no']
#             )
#             # Log the user in immediately after registration
#             login(request, user)
#             return redirect('doctor_register_step2')
#     else:
#         form = DoctorRegistrationForm1()
#     return render(request, 'user_auth/doctor_register_step1.html', {'form': form})

# Doctor Registration Step 2 - Specializations

@login_required
def doctor_register_step2(request):
    try:
        doctor = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_register_step1')

    if doctor.registration_step < 1:  # Ensure step 1 is completed
        return redirect('doctor_register_step1')

    if request.method == 'POST':
        form = DoctorRegistrationForm2(request.POST)
        if form.is_valid():
            specializations = form.cleaned_data['specializations'].split('\n')
            for spec in specializations:
                Specialization.objects.create(doctor=doctor, name=spec.strip())

            doctor.registration_step = 2  # Update step progress
            doctor.save()
            return redirect('doctor_register_step3')
    else:
        form = DoctorRegistrationForm2()

    return render(request, 'user_auth/doctor_register_step2.html', {'form': form})

# Doctor Registration Step 3 - Practice Details
@login_required
def doctor_register_step3(request):
    try:
        doctor = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_register_step1')

    if doctor.registration_step < 2:  # Ensure step 2 is completed
        return redirect('doctor_register_step2')

    if request.method == 'POST':
        form = DoctorRegistrationForm3(request.POST)
        if form.is_valid():
            practice_detail = form.save(commit=False)
            practice_detail.doctor = doctor
            practice_detail.save()

            doctor.registration_step = 3  # Update step progress
            doctor.save()
            return redirect('doctor_register_step4')
    else:
        form = DoctorRegistrationForm3()

    return render(request, 'user_auth/doctor_register_step3.html', {'form': form})

# Doctor Registration Step 4 - Online Clinic
@login_required
def doctor_register_step4(request):
    # Redirect if the user hasn't completed previous steps
    try:
        doctor = request.user.doctorprofile
        if doctor.registration_step < 3:
            return redirect('doctor_register_step3')
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_register_step1')

    if request.method == 'POST':
        form = DoctorRegistrationForm4(request.POST)
        if form.is_valid():
            online_clinic = form.save(commit=False)
            online_clinic.doctor = doctor
            online_clinic.save()
            # Update the registration step
            doctor.registration_step = 4
            doctor.save()
            return redirect('doctor_register_step5')
    else:
        form = DoctorRegistrationForm4()
    return render(request, 'user_auth/doctor_register_step4.html', {'form': form})

# Doctor Registration Step 5 - Profile Picture
@login_required
def doctor_register_step5(request):
    # Redirect if the user hasn't completed previous steps
    try:
        doctor = request.user.doctorprofile
        if doctor.registration_step < 4:
            return redirect('doctor_register_step4')
    except DoctorProfile.DoesNotExist:
        return redirect('doctor_register_step1')

    if request.method == 'POST':
        form = DoctorRegistrationForm5(request.POST, request.FILES)
        if form.is_valid():
            doctor.profile_picture = form.cleaned_data['profile_picture']
            doctor.registration_step = 5
            doctor.save()
            messages.success(request, 'Registration complete. Please wait for admin verification.')
            return redirect('doctor_dashboard')
    else:
        form = DoctorRegistrationForm5()
    return render(request, 'user_auth/doctor_register_step5.html', {'form': form})

# @login_required
# def dashboard(request):
#     if hasattr(request.user, 'patientprofile'):
#         return render(request, 'user_auth/patient_dashboard.html')
#     elif hasattr(request.user, 'doctorprofile'):
#         return render(request, 'user_auth/doctor_dashboard.html')
#     return redirect('home')
# user_auth/views.py


@login_required
def dashboard(request):
    if hasattr(request.user, 'patientprofile'):
        return render(request, 'user_auth/patient_dashboard.html')
    elif hasattr(request.user, 'doctorprofile'):
        doctor_profile = request.user.doctorprofile
        return render(request, 'user_auth/doctor_dashboard.html', {'doctor_profile': doctor_profile})
    return redirect('home')
