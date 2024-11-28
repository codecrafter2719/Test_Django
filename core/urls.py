from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from user_auth import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('guest_access.urls')),

    # path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='user_auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('doctor/register/step1/', views.doctor_register_step1, name='doctor_register_step1'),
    path('doctor/register/step2/', views.doctor_register_step2, name='doctor_register_step2'),
    path('doctor/register/step3/', views.doctor_register_step3, name='doctor_register_step3'),
    path('doctor/register/step4/', views.doctor_register_step4, name='doctor_register_step4'),
    path('doctor/register/step5/', views.doctor_register_step5, name='doctor_register_step5'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Add this line

    path('dashboard/', views.dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

