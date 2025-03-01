from django.contrib import admin
from app.models import m_msgs, u_files, term_agree, m_contacts, OpenAIThread

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