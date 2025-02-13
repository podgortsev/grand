from django.contrib import admin
from app.models import mod_msgs, temp_mod_msgs, user_files

class admin_mod_msgs(admin.ModelAdmin): 
    list_display = ('user_id','if_user', 'create_date', 'msg')

admin.site.register(mod_msgs,admin_mod_msgs)

class admin_temp_mod_msgs(admin.ModelAdmin): 
    list_display = ('user_id','if_user', 'create_date', 'msg')

admin.site.register(temp_mod_msgs,admin_temp_mod_msgs)

class admin_user_files(admin.ModelAdmin): 
    list_display = ('user_id','doc')

admin.site.register(user_files,admin_user_files)