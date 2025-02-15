from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from app.models import mod_msgs, user_files, term_agree
import openai
from django.contrib.auth import logout
import random
import string

# Set your OpenAI API Key
openai.api_key = ""

# Max file size allowed (in bytes), here it's set to 50MB
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def index(request):
    if 'user_logged_in' not in request.COOKIES:
        user_temp_id = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
        response.set_cookie('user_logged_in', user_temp_id, max_age=2147483647)
    
    user_status = request.COOKIES.get('user_logged_in')
    agreed = 1
    if term_agree.objects.filter(user_id=user_status).count()==0:
        agreed = 0

    msgs = mod_msgs.objects.filter(user_id=user_status)
    
    context_data = {
        'msgs': msgs,
        "agreed": agreed
    }
    
    response = render(request, 'index.html', context_data)    
    return response

def sendagreed(request):
    pass

@csrf_exempt    
def sendmsg(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    msg = request.POST.get("msg")
    if not msg:
        return JsonResponse({"error": "Message is required"}, status=400)

    m = mod_msgs()
    m.user_id = request.COOKIES['user_logged_in']
    m.if_user = True
    m.msg = msg
    m.save()

    files = request.FILES.getlist("files[]")
    if files:
        for uploaded_file in files:
            if uploaded_file.size > MAX_FILE_SIZE:
                return JsonResponse({"error": "File size exceeds 50MB limit"}, status=400)
            savefiles(uploaded_file, request.COOKIES['user_logged_in'])

    answer = askopenai(msg)    
    ans_tst = datetime.now().strftime("%I:%M %p")
    
    m = mod_msgs()
    m.user_id = request.COOKIES['user_logged_in']
    m.if_user = False
    m.msg = answer
    m.save()
    
    return JsonResponse({"message": answer, "tst": ans_tst}, status=200)

def askopenai(msg):
    return "LLM is still not working"

def savefiles(uploaded_file, uid):
    fname = ''.join(random.choices(string.ascii_letters + string.digits, k=25)) + "_" + uploaded_file.name
    m = user_files()
    m.user_id = uid
    m.doc_name = fname
    m.doc_url = ""  # Placeholder for actual file URL
    m.save()
    return "ok"

def terms(request):
    response = render(request, 'terms.html', {})    
    return response

def privacypolicy(request):
    response = render(request, 'privacypolicy.html', {})    
    return response

@csrf_exempt
def agreebtn(request):
    t = term_agree()
    t.user_id = request.COOKIES['user_logged_in']
    t.save()
    return JsonResponse({}, status=200)


"""
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
                    messages = mod_msgs.objects.filter(user_id=user_status) #temp

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

"""