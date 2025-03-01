from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from app.models import m_msgs, u_files, term_agree, m_contacts, OpenAIThread
import openai
from django.contrib.auth import logout
import random
import string
import time
import os
# Max file size allowed (in bytes), here it's set to 50MB
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def index(request):
    if 'user_logged_in' not in request.COOKIES:
        user_temp_id = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
        context_data = {
            'msgs': [],
            "agreed": 0,
            "firstmsg":return_static_msg(".")
        }
        response = render(request, 'index.html', context_data)
        response.set_cookie('user_logged_in', user_temp_id, max_age=2147483647)
        return response
    user_status = request.COOKIES.get('user_logged_in')
    agreed = 1
    if term_agree.objects.filter(user_id=user_status).count()==0:
        agreed = 0

    msgs = m_msgs.objects.filter(user_id=user_status)
    
    context_data = {
        'msgs': msgs,
        "agreed": agreed,
        "firstmsg":return_static_msg(".")
    }
    
    response = render(request, 'index.html', context_data)    
    return response

def contacts(request):
    if 'user_logged_in' not in request.COOKIES:
        user_temp_id = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
        context_data = {
            'contas': contas,
            "agreed": agreed
        }
        response = render(request, 'contacts.html', context_data)  
        response.set_cookie('user_logged_in', user_temp_id, max_age=2147483647)  
        return response
    
    user_status = request.COOKIES.get('user_logged_in')
    agreed = 1
    if term_agree.objects.filter(user_id=user_status).count()==0:
        agreed = 0

    contas = m_contacts.objects.filter(user_id=user_status)
    
    context_data = {
        'contas': contas,
        "agreed": agreed
    }
    
    response = render(request, 'contacts.html', context_data)    
    return response


def docs(request):
    if 'user_logged_in' not in request.COOKIES:
        user_temp_id = ''.join(random.choices(string.ascii_letters + string.digits, k=25))
        response.set_cookie('user_logged_in', user_temp_id, max_age=2147483647)
    
    user_status = request.COOKIES.get('user_logged_in')
    agreed = 1
    if term_agree.objects.filter(user_id=user_status).count()==0:
        agreed = 0

    docums = u_files.objects.filter(user_id=user_status)
    
    context_data = {
        'docums': docums,
        "agreed": agreed
    }
    
    response = render(request, 'contacts.html', context_data)    
    return response



@csrf_exempt    
def sendmsg(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    msg = request.POST.get("msg")
    if not msg:
        return JsonResponse({"error": "Message is required"}, status=400)

    m = m_msgs()
    m.user_id = request.COOKIES['user_logged_in']
    m.if_user = True
    m.msg = msg
    m.assistant_name = "0"
    m.save()

    files = request.FILES.getlist("files[]")
    if files:
        for uploaded_file in files:
            if uploaded_file.size > MAX_FILE_SIZE:
                return JsonResponse({"error": "File size exceeds 50MB limit"}, status=400)
            savefiles(uploaded_file, request.COOKIES['user_logged_in'])
    
    answer = askopenai(msg, request.COOKIES['user_logged_in'],0)    
    ans_tst = datetime.now().strftime("%I:%M %p")
    
    m = m_msgs()
    m.user_id = request.COOKIES['user_logged_in']
    m.if_user = False
    m.msg = answer[0]
    m.assistant_name = answer[1]
    m.save()
    
    return JsonResponse({"message": answer, "tst": ans_tst}, status=200)

openai.api_key = os.getenv('OPENAI_API_KEY')  # Replace with your OpenAI API key
#ASSISTANT_ID = os.getenv('ASSISTANT_ID')  # Replace with your OpenAI Assistant ID

def get_assistant_id_by_name(assistant_name):
    assistant_name = "assistant_" + assistant_name
    assistants = openai.beta.assistants.list().data  # Get list of assistants
    for assistant in assistants:
        if assistant.name == assistant_name:
            return assistant.id
    return None  # Return None if no match is found

def return_static_msg(id):
    static_ans = {
        ".":"",
        "a":"",
        "b":"",
        "c":"",
        "d":""
        }
    return static_ans[id]

def askopenai(msg, user_id, typ):
    # Check if user has an existing thread
    thread = OpenAIThread.objects.filter(user_id=user_id).first()
    
    if not thread:
        # Create a new thread if one does not exist
        thread_response = openai.beta.threads.create()
        thread = OpenAIThread.objects.create(user_id=user_id, thread_id=thread_response.id,assistant_name="1")

    ans_assist = thread.assistant_name
    # Send user message to OpenAI Assistant
    openai.beta.threads.messages.create(
        thread_id=thread.thread_id,
        role="user",
        content=msg
    )

    # Run Assistant processing
    run_response = openai.beta.threads.runs.create(
        thread_id=thread.thread_id,
        assistant_id=get_assistant_id_by_name(thread.assistant_name)
    )

    # Wait for completion
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread.thread_id,
            run_id=run_response.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)  # Avoid excessive API calls

    # Retrieve messages and extract Assistant's response
    messages = openai.beta.threads.messages.list(thread_id=thread.thread_id)
    ai_response = "I'm sorry, I couldn't process that."
    for msg in messages.data:
        if msg.role == 'assistant':
            try:
                ai_response = msg.content[0].text.value
                break
            except:
                pass
    
    new_assistant_name_index = ai_response.find(';')
    new_assistant_name = ai_response[:new_assistant_name_index].strip()
    ans_msg = ai_response[new_assistant_name_index + 1:].strip()
    if new_assistant_name_index!="0":
        try:
            tryint = int(new_assistant_name)
            thread_response = openai.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": ans_msg  # Add summary as the first message
                    }
                ]
            )
            if typ==1:
                return ["please try again"+ai_response,"1"]
            thread = OpenAIThread.objects.filter(user_id=user_id).first()
            thread.thread_id = thread_response.id
            thread.assistant_name = new_assistant_name
            thread.save()
            ans_msg = askopenai(msg, user_id, 1)
            ans_assist = new_assistant_name

        except ValueError:
            ans_msg = return_static_msg(new_assistant_name)
    return [ans_msg,ans_assist]

def savefiles(uploaded_file, uid):
    fname = ''.join(random.choices(string.ascii_letters + string.digits, k=25)) + "_" + uploaded_file.name
    m = u_files()
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

@csrf_exempt
def sendcontact(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    m = m_contacts()
    m.user_id = request.COOKIES['user_logged_in']
    m.name = request.POST.get("name")
    m.email = request.POST.get("email")
    m.type = request.POST.get("type")
    m.title = request.POST.get("title")
    m.save()
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
                    messages = m_msgs.objects.filter(user_id=user_status) #temp

                    for msg in messages:
                        m_msgs.objects.create(
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