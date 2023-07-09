from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from .models import Message
from .forms import SignUpForm
from .serializers import MessageSerializer, UserSerializer


def IndexView(request):
    if request.user.is_authenticated:
        return redirect('chats')
    
    if request.method == 'GET':
        return render(request, 'index.html', {})
    
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('chats')
        else:
            return HttpResponse('{"error": "User does not exist"}')


def LogoutView(request):
    logout(request)
    return redirect('/')


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender,
            receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, 
            context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('/')
    
    if request.method == "GET":
        usernames = {
            "users": User.objects.exclude(username=request.user.username)
        }
        return render(request, "chat.html", context=usernames)


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "GET":

        info = {
            "users": User.objects.exclude(username=request.user.username),
            "receiver": User.objects.get(id=receiver),
            "messages": Message.objects.filter(
                sender_id=sender, receiver_id=receiver) | 
            Message.objects.filter(sender_id=receiver, receiver_id=sender),
        }
        return render(request, "messages.html", context=info)
    

def register_view(request):
    """ Render registration page """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1'] 

            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chats')
    else:
        form = SignUpForm()
        
    return render(request, 'register.html', {'form': form})   