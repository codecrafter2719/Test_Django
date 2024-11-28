from django.shortcuts import redirect
from django.urls import reverse

class RestrictUnapprovedDoctorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'doctorprofile'):
            doctor_profile = request.user.doctorprofile
            if not doctor_profile.is_approved and request.path not in [reverse('logout'), reverse('doctor_dashboard')]:
                return redirect('doctor_dashboard')
        return self.get_response(request)
