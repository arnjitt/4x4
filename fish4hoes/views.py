import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Friend, Chat, Message, Event, Carpool, CarpoolRider
from .forms import FriendForm, FriendEnergyFormSet

# format line

@require_POST
@csrf_exempt
def update_carpool_riders(request):
	"""
	Expected JSON body:
	{
		"carpool_id": 1,
		"friends_ids": [2,3,4]
	}
	"""
	data = json.loads(request.body("utf-8"))

	carpool_id = data["carpool_id"]
	friends_ids = data["friend_ids"]

	carpool = Carpool.objects.get(pk=carpool_id)

	# removes riders not in the new list
	CarpoolRider.objects.filter(carpool=carpool).exclude(
		friend_id__in=friend_ids
	).delete()

	for fid in friend_ids:
		CarpoolRider.objects.get_or_create(
			carpool=carpool, 
			friend_id=fid,
		)

	return JsonResponse({"status": "ok"})



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
	chat, _ = Chat.objects.get_or_create(name="general")

	if request.method == "POST":
		sender_id = request.POST.get("sender_id")
		text = request.POST.get("text", "").strip()

		if sender_id and text:
			sender = get_object_or_404(Friend, id=sender_id)
			Message.objects.create(
				text=text,
				sender=sender,
				chat=chat,
			)
		return redirect("chat_room")

	
	friends_qs = Friend.objects.all()
	friends_with_colors = assign_friend_colors(friends_qs)

	messages = (
		Message.objects
		.filter(chat=chat)
		.select_related("sender")
		.order_by("created_at", "id")
	)

	return render(
		request,
		"website/chat_room.html",
		{
			"friends_with_colors": friends_with_colors,
			"friends": friends_qs,
			"messages": messages,
		},
	)

## Page Logic held for adding Friends to database
def add_friend(request):
	qs = Friend.objects.all()
	messages = demo_messages()
	chat, _ = Chat.objects.get_or_create(name="general")
	mini_messages = (
		Message.objects
		.filter(chat=chat)
		.select_related("sender")
		.order_by("created_at", "id")
	)
	# friend look up and DELETE
	if request.method == "POST":
		if "delete_friend_id" in request.POST:
			friend_id = request.POST.get("delete_friend_id")
			friend = get_object_or_404(Friend, id=friend_id)
			friend.delete()
			return redirect("add_friend")

		# message delete function
		if "delete_message_id "in request.POST:
			msg_id = request.POST.get("delete_message_id")
			msg = get_object_or_404(Message, id=msg_id)
			msg.delete()
			return redirect("add_friend")
		
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
		"messages": mini_messages,
		"friends": qs,
	})

def plan_event(request):
	event, _ = Event.objects.get_or_create(
		trip_id="basketball-trip",
		defaults={"name": "Basketball Trip"}
	)
	friends_qs = Friend.objects.all()
	friends_with_colors = assign_friend_colors(friends_qs)

	carpools = (
		Carpool.objects
		.filter(event=event)
		.prefetch_related("riders__friend", "driver")
	)
	event_name = "Basketball Trip"
	chat, _ = Chat.objects.get_or_create(name="general")
	mini_messages = (
		Message.objects
		.filter(chat=chat)
		.select_related("sender")
		.order_by("created_at", "id")
	)
	return render(request, "website/plan_event.html", {
			"event": event,
			"friends_with_colors": friends_with_colors,
			"carpools": carpools,
			"event_name": event_name,
			"mini_messages": mini_messages,
	})