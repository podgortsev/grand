from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
from app.models import mod_msgs, temp_mod_msgs, user_files
import openai
from django.contrib.auth import logout
import random
import string

openai.api_key=""

def home(request):
    if request.user.is_authenticated:
        u_doc = user_files.objects.filter(user_id=request.user.id)
        if(u_doc.count()==0):
            cou_doc=0
        else:
            cou_doc=1

        if request.user.last_name == "":
            msgs = mod_msgs.objects.filter(user_id = request.user.id)
            if msgs.count()>20:
                context_data = {
                    'msgs': msgs,
                    "type":4,
                    "cou_doc":cou_doc
                }
            else:
                context_data = {
                    'msgs': msgs,
                    "type":3,
                    "cou_doc":cou_doc
                }
            response = render(request, 'home.html', context_data)
        else:
            pass 
    else:
        if 'user_logged_in' in request.COOKIES:
            user_status = request.COOKIES['user_logged_in']
            msgs = temp_mod_msgs.objects.filter(user_id = user_status)
            if msgs.count()>10:
                context_data = {
                    'msgs': msgs,
                    "type":2
                }
            else:
                context_data = {
                    'msgs': msgs,
                    "type":1
                }
            response = render(request, 'home.html', context_data)
        else:
            user_temp_id = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
            context_data = {
                "type":1,
                'msgs':[]
            }        
            response = render(request, 'home.html', context_data)
            response.set_cookie('user_logged_in', user_temp_id, max_age=2147483647)
    return response

@csrf_exempt
def signup(request):
    try:
        if request.method == 'POST':
            if not User.objects.filter(username = request.POST["email"]).exists():
                user = User.objects.create_user(username=request.POST["email"],
                                        email=request.POST["email"],
                                        password=request.POST["password"],
                                        first_name=request.POST["name"])
                user = authenticate(request, username=request.POST["email"],
                                    password=request.POST["password"])
                login(request, user)
                user_status = request.COOKIES['user_logged_in']
                if user_status:
                    messages = temp_mod_msgs.objects.filter(user_id=user_status)

                    for msg in messages:
                        mod_msgs.objects.create(
                            user_id=user.id,
                            if_user=msg.if_user,
                            create_date=msg.create_date,  # Optional, Django auto-generates this
                            msg=msg.msg
                        )
            else:
                return login(request)
            
        return JsonResponse({"message": "Ok"}, status=200)
    except Exception as e: 
        return JsonResponse({"message": str(e)}, status=400)
    
@csrf_exempt
def logindef(request):
    try:
        if request.method == 'POST':
            user = authenticate(request, username=request.POST["email"],
                                password=request.POST["password"])
            login(request, user)
            
        return JsonResponse({"message": "Ok"}, status=200)
    except Exception as e: 
        return JsonResponse({"message": str(e)}, status=400)

@csrf_exempt    
def sendmsg(request):
    msg = request.POST["msg"]
    tst = request.POST["tst"]
    type = request.POST["type"]
    if type=="1":
        m = temp_mod_msgs()
        m.user_id = request.COOKIES['user_logged_in']
        m.if_user = True
        m.msg = msg
        m.save()
        
        if temp_mod_msgs.objects.filter(user_id = request.COOKIES['user_logged_in'],if_user=True).count()>5:
            return JsonResponse({"status":"limit1"}, status=200)
        else:
            #openai
            try:
                # Make a request to the GPT-3.5 (or GPT-4 if available) model
                response = openai.completions.create(
                    model="gpt-3.5-turbo",  # or another model available to you (e.g., gpt-4)
                    prompt=msg,
                    max_tokens=100
                )
                answer = response['choices'][0]['message']['content']
            except Exception as e:
                return JsonResponse({"message": str(e),"status":"error"}, status=200)
            ans_tst = datetime.now().strftime("%I:%M %p")
            m = mod_msgs()
            m.user_id = request.user.id
            m.if_user = False
            m.msg = answer
            m.save()
            return JsonResponse({"message": answer,"tst":ans_tst,"status":"ok1"}, status=200)
    else:
        m = mod_msgs()
        m.user_id = request.user.id
        m.if_user = True
        m.msg = msg
        m.save()
        if mod_msgs.objects.filter(user_id = request.user.id,if_user=True).count()>10:
            return JsonResponse({"status":"limit2"}, status=200)
        else:
            #openai
            try:
                # Make a request to the GPT-3.5 (or GPT-4 if available) model
                response = openai.completions.create(
                    model="gpt-3.5-turbo",  # or another model available to you (e.g., gpt-4)
                    prompt=msg,
                    max_tokens=100
                )
                answer = response['choices'][0]['message']['content']
            except Exception as e:
                return JsonResponse({"message": str(e),"status":"error"}, status=200)
            ans_tst = datetime.now().strftime("%I:%M %p")
            m = mod_msgs()
            m.user_id = request.user.id
            m.if_user = False
            m.msg = answer
            m.save()
            return JsonResponse({"message": answer,"tst":ans_tst,"status":"ok"}, status=200)

@csrf_exempt 
def logoutdef(request):
    logout(request)
    return JsonResponse({"status":"ok"}, status=200)

@csrf_exempt 
def adddoc(request):
    link = request.POST["link"]
    u = user_files()
    u.user_id = request.user.id
    u.doc = link
    u.save()
    return JsonResponse({"status":"ok"}, status=200)