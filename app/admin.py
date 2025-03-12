from django.contrib import admin
from django import forms
from app.models import m_msgs, u_files, term_agree, m_contacts, OpenAIThread, Company, Client, ClientAppointmentHistory, ClientReportHistory
from django.utils.html import format_html
from django.utils import timezone
from app.views import custom_admin_page
from django.urls import path


class admin_m_msgs(admin.ModelAdmin): 
    list_display = ('user_id','if_user', 'assistant_name','create_date', 'msg')

admin.site.register(m_msgs,admin_m_msgs)

class admin_u_files(admin.ModelAdmin): 
    list_display = ('user_id','doc_name','doc_url')

admin.site.register(u_files,admin_u_files)

class admin_term_agree(admin.ModelAdmin): 
    list_display = ('user_id','create_date')

admin.site.register(term_agree,admin_term_agree)

class admin_contacts(admin.ModelAdmin): 
    list_display = ('user_id','create_date','name','email','type','title')

admin.site.register(m_contacts,admin_contacts)

class admin_OpenAIThread(admin.ModelAdmin): 
    list_display = ('user_id','thread_id','created_at','assistant_name')

admin.site.register(OpenAIThread,admin_OpenAIThread)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "website")

    # Hide the user field from the form
    def get_exclude(self, request, obj=None):
        return ("user",)

    # Automatically assign the logged-in user on save
    def save_model(self, request, obj, form, change):
        if not obj.user:  # Set only if it's a new object
            obj.user = request.user
        obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Allow superusers to see all records
        return qs.filter(user=request.user)

class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = "__all__"
  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default company as the first one in the list
        if Company.objects.exists():
            self.fields["company"].initial = Company.objects.first().id
     
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = ("name", "next_appointment_status", "last_report_status")
    search_fields = ("name", "phone_number", "email")
    list_filter = ("company",)

    class Media:
        js = ("admin/js/myclient.js",) 

    fieldsets = (
        (None, {
            'fields': ('name', 'phone_number','company')  # First section
        }),
        ('Visit Info', {
            'fields': ('next_appointment', 'last_report')  # Second section
        }),
        ('Additional Info', {
            'fields': ('email', ),  # Third section
        }),
        ('Current status', {
            'fields': ('create_date', ),  # Third section
        }),
    )

    exclude = ('user',)  # Hide the 'user' field

    # Custom method for displaying next_appointment status
    def next_appointment_status(self, obj):
        if obj.next_appointment is None or obj.next_appointment < timezone.now():
            return format_html(
                '<span style="color: red;">Please provide (Invalid or past date)</span>'
            )
        return obj.next_appointment

    next_appointment_status.short_description = "Next Appointment"

    # Custom method for displaying last_report status
    def last_report_status(self, obj):
        if obj.last_report is None or obj.last_report == '' or obj.last_report == '-':
            return format_html(
                '<span style="color: red;">Please provide</span>'
            )
        return obj.last_report.name  # Return the filename of the uploaded file

    last_report_status.short_description = "Last Report"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Allow superusers to see all records
        return qs.filter(user=request.user)
    
    # Automatically assign the logged-in user on save
    def save_model(self, request, obj, form, change):
        if not obj.user:  # Set only if it's a new object
            obj.user = request.user
        super().save_model(request, obj, form, change)

class ClientAppointmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'appointment_datetime', 'create_date', 'user')
    search_fields = ('client__name', 'appointment_datetime')
    list_filter = ('create_date', 'user')

class ClientReportHistoryAdmin(admin.ModelAdmin):
    list_display = ('client', 'report_file', 'create_date', 'user')
    search_fields = ('client__name', 'report_file')
    list_filter = ('create_date', 'user')

admin.site.register(ClientAppointmentHistory, ClientAppointmentHistoryAdmin)
admin.site.register(ClientReportHistory, ClientReportHistoryAdmin)