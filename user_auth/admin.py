from django.contrib import admin
from .models import PatientProfile, DoctorProfile, Specialization, Qualification, Experience, PracticeDetail, OnlineClinic

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'pmdc_no', 'is_verified', 'is_approved')
    list_filter = ('is_verified', 'is_approved')
    search_fields = ('user__username', 'full_name', 'pmdc_no')
    actions = ['verify_doctors', 'approve_doctors']

    def verify_doctors(self, request, queryset):
        """
        Admin action to verify selected doctors' PMDC numbers.
        """
        queryset.update(is_verified=True)
        self.message_user(request, "Selected doctors have been marked as PMDC verified.")
    verify_doctors.short_description = "Mark selected doctors as PMDC verified"

    def approve_doctors(self, request, queryset):
        """
        Admin action to approve selected doctors' profiles.
        """
        queryset.update(is_approved=True)
        self.message_user(request, "Selected doctors have been approved.")
    approve_doctors.short_description = "Approve selected doctors"

# Register other models
admin.site.register(PatientProfile)
admin.site.register(Specialization)
admin.site.register(Qualification)
admin.site.register(Experience)
admin.site.register(PracticeDetail)
admin.site.register(OnlineClinic)
