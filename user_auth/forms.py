# user_auth/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PatientProfile, DoctorProfile, Specialization, Qualification, Experience, PracticeDetail, OnlineClinic

class PatientRegistrationForm(UserCreationForm):
    phone_no = forms.CharField(max_length=15)
    full_name = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class DoctorRegistrationForm1(UserCreationForm):
    phone_no = forms.CharField(max_length=15)
    full_name = forms.CharField(max_length=100)
    pmdc_no = forms.CharField(max_length=50)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class DoctorRegistrationForm2(forms.Form):
    specializations = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',  # Bootstrap class for styling
                'placeholder': 'Enter each specialization on a new line',  # User-friendly placeholder text
                'rows': 5,  # Sets the height of the textarea
                'style': 'resize: vertical;',  # Allows vertical resizing only
            }
        ),
        help_text="Enter each specialization on a new line.",
        label="Specializations",  # Descriptive label
    )  
    # Dynamic form fields for qualifications and experiences will be handled in the view

class DoctorRegistrationForm3(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'}),
        input_formats=['%I:%M %p', '%H:%M'],  # Allows both "10:00 AM" and "18:00"
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'}),
        input_formats=['%I:%M %p', '%H:%M'],
    )

    class Meta:
        model = PracticeDetail
        fields = '__all__'
        exclude = ('doctor',)
        widgets = {
            'days': forms.CheckboxSelectMultiple(choices=PracticeDetail.DAYS_CHOICES),
        }



class DoctorRegistrationForm4(forms.ModelForm):
    start_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'}),
        input_formats=['%I:%M %p', '%H:%M'],  # Allows both "10:00 AM" and "18:00"
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(format='%I:%M %p', attrs={'placeholder': 'HH:MM AM/PM'}),
        input_formats=['%I:%M %p', '%H:%M'],
    )

    class Meta:
        model = OnlineClinic
        fields = '__all__'
        exclude = ('doctor',)
        widgets = {
            'days': forms.CheckboxSelectMultiple(choices=PracticeDetail.DAYS_CHOICES)
        }

class DoctorRegistrationForm5(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ('profile_picture',)
