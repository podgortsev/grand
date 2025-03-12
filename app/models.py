from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
import json
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class m_msgs(models.Model):
    user_id = models.CharField(max_length=255)
    if_user = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    msg = models.TextField()
    assistant_name = models.CharField(default="0",null=True)

class u_files(models.Model):
    user_id = models.CharField(max_length=255)
    doc_name = models.CharField(max_length=2000)
    doc_url = models.CharField(max_length=2048)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class term_agree(models.Model):
    user_id = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class m_contacts(models.Model):
    user_id = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

class OpenAIThread(models.Model):
    user_id = models.CharField(max_length=255, unique=True)  # Unique thread per user
    thread_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assistant_name = models.CharField(default="1",null=True)

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to="company_logos/", blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    next_appointment = models.DateTimeField(null=True, blank=True)
    last_report = models.FileField(upload_to='client_reports/', null=True, blank=True)
    create_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)

    def __str__(self):
        return f"{self.name} ({self.company.name})"
    
class ClientAppointmentHistory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="appointments_history")
    appointment_datetime = models.DateTimeField()
    create_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Appointment for {self.client.name} on {self.appointment_datetime}"

class ClientReportHistory(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="reports_history")
    report_file = models.FileField(upload_to='client_reports_history/')
    create_date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Report for {self.client.name} uploaded on {self.create_date}"
    
    def save(self, *args, **kwargs):
        # Save the Client instance first
        super().save(*args, **kwargs)

        # Create appointment history if next_appointment is set
        if self.next_appointment:
            ClientAppointmentHistory.objects.create(
                client=self,
                appointment_datetime=self.next_appointment,
                user=self.user,
            )

        # Create report history if last_report is set
        if self.last_report:
            ClientReportHistory.objects.create(
                client=self,
                report_file=self.last_report,
                user=self.user,
            )