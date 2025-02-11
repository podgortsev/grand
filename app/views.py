from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, time
from app.models import mod_msgs
import openai
from django.contrib.auth import logout

openai.api_key=""

def home(request):
    if request.user.is_authenticated:
        msgs = mod_msgs.objects.filter(user_id = request.user.id)
        context = {
            'msgs': msgs,
        }
        return render(request, 'home.html', context)

    else:
        template = loader.get_template("auth.html")
    return HttpResponse(template.render())

@csrf_exempt
def signup(request):
    try:
        if request.method == 'POST':
            if not User.objects.filter(username = request.POST["email"]).exists():
                user = User.objects.create_user(username=request.POST["email"],
                                        email=request.POST["visitedDoctor"],
                                        password=request.POST["password"],
                                        first_name=request.POST["name"],
                                        last_name=request.POST["documentsLink"])
                user = authenticate(request, username=request.POST["email"],
                                    password=request.POST["password"])
                login(request, user)
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
    m = mod_msgs()
    m.user_id = request.user.id
    m.if_user = True
    m.msg = msg
    m.save()
    
    #check if limit
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    today_start = datetime.combine(today, time.min)
    today_end = datetime.combine(tomorrow, time.min)
    if mod_msgs.objects.filter(user_id = request.user.id,create_date__gte=today_start,create_date__lt=today_end).count()>10:
        answer = "You reached your limit"
        ans_tst = datetime.now().strftime("%I:%M %p")
        m = mod_msgs()
        m.user_id = request.user.id
        m.if_user = False
        m.msg = answer
        m.save()
        return JsonResponse({"message": answer,"tst":ans_tst,"status":"limit"}, status=200)
    
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