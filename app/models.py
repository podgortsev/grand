from django.db import models
from django.utils.timezone import now

class m_msgs(models.Model):
    user_id = models.CharField(max_length=255)
    if_user = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    msg = models.TextField()

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


