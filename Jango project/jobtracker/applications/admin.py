from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Company, JobApplication, TrackedCompany, JobPosting


# Customize the admin site header and title
admin.site.site_header = "🎯 Job Tracker Administration"
admin.site.site_title = "Job Tracker Admin"
admin.site.index_title = "Welcome to Job Tracker Admin Panel"


# Enhanced Company Admin
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'application_count']
    search_fields = ['name']
    
    def application_count(self, obj):
        return obj.jobapplication_set.count()
    application_count.short_description = 'Total Applications'


# Enhanced Job Application Admin
@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['company', 'role', 'user', 'status', 'deadline', 'applied_date']
    list_filter = ['status', 'applied_date', 'deadline']
    search_fields = ['company__name', 'role', 'user__username']
    date_hierarchy = 'applied_date'
    
    fieldsets = (
        ('Application Details', {
            'fields': ('user', 'company', 'role')
        }),
        ('Status & Dates', {
            'fields': ('status', 'deadline', 'applied_date')
        }),
    )
    
    readonly_fields = ['applied_date']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is not superuser, show only their applications
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs


# Enhanced Tracked Company Admin
@admin.register(TrackedCompany)
class TrackedCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'career_url', 'job_count']
    list_filter = ['user']
    search_fields = ['name', 'user__username']
    
    def job_count(self, obj):
        return obj.jobposting_set.count()
    job_count.short_description = 'Job Postings Found'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is not superuser, show only their tracked companies
        if not request.user.is_superuser:
            return qs.filter(user=request.user)
        return qs


# Enhanced Job Posting Admin
@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ['title', 'tracked_company', 'company_user', 'created_at']
    list_filter = ['created_at', 'tracked_company']
    search_fields = ['title', 'tracked_company__name']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
    
    def company_user(self, obj):
        return obj.tracked_company.user.username
    company_user.short_description = 'User'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # If user is not superuser, show only their job postings
        if not request.user.is_superuser:
            return qs.filter(tracked_company__user=request.user)
        return qs


# Customize User Admin to show job tracker related info
class JobTrackerUserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ('application_count', 'tracked_company_count')
    
    def application_count(self, obj):
        return obj.jobapplication_set.count()
    application_count.short_description = 'Applications'
    
    def tracked_company_count(self, obj):
        return obj.trackedcompany_set.count()
    tracked_company_count.short_description = 'Tracked Companies'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, JobTrackerUserAdmin)