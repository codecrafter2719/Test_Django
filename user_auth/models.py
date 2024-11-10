#  user_auth/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15)
    full_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=15)
    full_name = models.CharField(max_length=100)
    pmdc_no = models.CharField(max_length=50, unique=True)
    is_verified = models.BooleanField(default=False)
    registration_step = models.IntegerField(default=1)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username

class Specialization(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Qualification(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)

class Experience(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200)

class PracticeDetail(models.Model):
    DAYS_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    doctor = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200)
    review_address = models.TextField()
    days = models.CharField(max_length=50)  # Store as comma-separated values
    start_time = models.TimeField()
    end_time = models.TimeField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    assistant_name = models.CharField(max_length=100)
    assistant_phone = models.CharField(max_length=15)

class OnlineClinic(models.Model):
    doctor = models.OneToOneField(DoctorProfile, on_delete=models.CASCADE)
    days = models.CharField(max_length=50)  # Store as comma-separated values
    start_time = models.TimeField()
    end_time = models.TimeField()
    online_consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
