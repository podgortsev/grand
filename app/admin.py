from django.contrib import admin
from app.models import mod_msgs, user_files, term_agree

class admin_mod_msgs(admin.ModelAdmin): 
    list_display = ('user_id','if_user', 'create_date', 'msg')

admin.site.register(mod_msgs,admin_mod_msgs)

class admin_user_files(admin.ModelAdmin): 
    list_display = ('user_id','doc_name','doc_url')

admin.site.register(user_files,admin_user_files)

class admin_term_agree(admin.ModelAdmin): 
    list_display = ('user_id','create_date')

admin.site.register(term_agree,admin_term_agree)