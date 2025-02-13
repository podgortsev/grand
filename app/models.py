from django.db import models

class mod_msgs(models.Model):
    user_id = models.IntegerField()
    if_user = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()

class temp_mod_msgs(models.Model):
    user_id = models.CharField(max_length=255)
    if_user = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()

class user_files(models.Model):
    user_id = models.IntegerField()
    doc = models.TextField()