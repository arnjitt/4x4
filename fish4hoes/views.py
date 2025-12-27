from django.shortcuts import render
from .models import Friend
def fishington_home(request):
  return render(request, "website/fishington.html")

def crewLive(request):
  return render(request, "website/crewLive.html")

def projectsPage(request):
  return render(request, "website/projects.html")

def chat_room(request):
  friends = Friend.objects.all()
  # sample messages // not from DB
  messages = [
    {"author": "System", "text": "Welcome to 4x4 demo"},
    {"author": "Cass", "text": "I love Overwatch!!!"},
    {"author": "Bryan", "text": "Ohhhhhahhhahhhahhhah"},
    {"author": "Mikey", "text": "Toughness"},
  ]
  return render(request, "website/chat_room.html", {"friends": friends, "messages": messages})
