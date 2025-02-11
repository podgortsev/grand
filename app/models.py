from django.db import models

class mod_msgs(models.Model):
    user_id = models.IntegerField()
    if_user = models.BooleanField()
    create_date = models.DateTimeField(auto_now_add=True)
    msg = models.TextField()