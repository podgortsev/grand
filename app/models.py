from django.db import models

class mod_msgs(models.Model):
    user_id = models.CharField(max_length=255)
    if_user = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()

class user_files(models.Model):
    user_id = models.CharField(max_length=255)
    doc_name = models.CharField(max_length=2000)
    doc_url = models.CharField(max_length=2048)

class term_agree(models.Model):
    user_id = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)