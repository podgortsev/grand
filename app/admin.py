from django.contrib import admin
from app.models import m_msgs, u_files, term_agree, mod_contacts

class admin_m_msgs(admin.ModelAdmin): 
    list_display = ('user_id','if_user', 'create_date', 'msg')

admin.site.register(m_msgs,admin_m_msgs)

class admin_u_files(admin.ModelAdmin): 
    list_display = ('user_id','doc_name','doc_url')

admin.site.register(u_files,admin_u_files)

class admin_term_agree(admin.ModelAdmin): 
    list_display = ('user_id','create_date')

admin.site.register(term_agree,admin_term_agree)

class admin_contacts(admin.ModelAdmin): 
    list_display = ('user_id','create_date','name','email','type','title')

admin.site.register(mod_contacts,admin_contacts)