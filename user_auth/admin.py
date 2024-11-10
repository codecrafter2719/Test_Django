# user_auth/admin.py
from django.contrib import admin
from .models import PatientProfile, DoctorProfile, Specialization, Qualification, Experience, PracticeDetail, OnlineClinic

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'pmdc_no', 'is_verified', 'registration_step')
    list_filter = ('is_verified', 'registration_step')
    search_fields = ('user__username', 'full_name', 'pmdc_no')
    actions = ['verify_doctors']

    def verify_doctors(self, request, queryset):
        queryset.update(is_verified=True)
    verify_doctors.short_description = "Verify selected doctors"

admin.site.register(PatientProfile)
admin.site.register(Specialization)
admin.site.register(Qualification)
admin.site.register(Experience)
admin.site.register(PracticeDetail)
admin.site.register(OnlineClinic)
