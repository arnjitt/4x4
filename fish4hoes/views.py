from django.shortcuts import render, redirect
from .models import Friend
from .forms import FriendForm, FriendEnergyFormSet



def fishington_home(request):
  return render(request, "website/fishington.html")

def crewLive(request):
  return render(request, "website/crewLive.html")

def projectsPage(request):
  return render(request, "website/projects.html")

FRIEND_COLORS = [
  "red",
  "blue",
  "green",
  "black",
  "orange",
  "teal",
  "limegreen",
  "purple",
  "grey",
  "brown",
]

def demo_messages():
  return [
    {"author": "System", "text": "Welcome to 4x4 demo"},
    {"author": "Cass", "text": "I love Overwatch!!!"},
    {"author": "Bryan", "text": "Ohhhhhahhhahhhahhhah"},
    {"author": "Mikey", "text": "Toughness"},
    {"author": "System", "text": "These are demonstration messages via demo_messages()"},
  ]

def assign_friend_colors(friends):
  colored = []
  palette_len = len(FRIEND_COLORS)
  for idx, friend in enumerate(friends):
    color = FRIEND_COLORS[idx % palette_len]
    colored.append((friend,color))
  return colored

def chat_room(request):
  friends_qs = Friend.objects.all()
  friends_with_colors = assign_friend_colors(friends_qs)
  # sample messages // not from DB
  messages = demo_messages()
  return render(
    request, 
    "website/chat_room.html", 
    {
      "friends_with_colors": friends_with_colors, 
      "messages": messages
    }
  )


## Page Logic held for adding Friends to database
def add_friend(request):
  qs = Friend.objects.all()
  messages = demo_messages()
  if request.method == "POST":
    friend_form = FriendForm(request.POST, prefix="new")
    formset = FriendEnergyFormSet(
      request.POST, 
      queryset=qs, 
      prefix="energy"
    )

    if "save_new" in request.POST and friend_form.is_valid():
      friend_form.save()
      return redirect("add_friend")
    
    if "save_energy" in request.POST and formset.is_valid():
      formset.save()
      return redirect("add_friend")
  else:
      friend_form = FriendForm(prefix="new")
      formset = FriendEnergyFormSet(queryset=qs, prefix="energy")

  return render(request, "website/add_friend.html", {
    "friend_form": friend_form,
    "formset": formset,
    "messages": messages,
  })

def plan_event(request):
    friends_qs = Friend.objects.all()
    friends_with_colors = assign_friend_colors(friends_qs)
    event_name = "Basketball Trip"
    messages = demo_messages()
    return render(
        request,
        "website/plan_event.html",
        {
            "friends_with_colors": friends_with_colors,
            "event_name": event_name,
            "messages": messages,
        },
    )