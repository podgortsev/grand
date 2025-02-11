from django.contrib import admin
from app.models import mod_msgs

class admin_mod_msgs(admin.ModelAdmin): 
    list_display = ('user_id','if_user', 'create_date', 'msg')

admin.site.register(mod_msgs,admin_mod_msgs)