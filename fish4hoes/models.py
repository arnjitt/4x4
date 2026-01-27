from django.db import models
from django.utils import timezone

class Event(models.Model):
	TRIP = "trip"
	PARTY = "party"
	MEAL = "meal"
	OTHER = "other"

	EVENT_TYPES = [
		(TRIP, "Trip"),
		(PARTY, "Party"),
		(MEAL, "Meal"),
		(OTHER, "Other"),
	]

	name = models.CharField(max_length=200)
	trip_id = models.SlugField(max_length=32, unique=True)
	event_type = models.CharField(
		max_length=10,
		choices=EVENT_TYPES,
		default=TRIP,
	)
	start_time = models.DateTimeField(default=timezone.now)
	location_name = models.CharField(max_length=100, blank=True)
	location_notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.name


class Friend(models.Model):
	ENERGY_LEVELS = [
	("low", "Low"),
	("medium", "Medium"),
	("high", "High")
	]
	name = models.CharField(max_length=100)
	energy = models.CharField(
		max_length=10,
		choices=ENERGY_LEVELS,
		default="medium"
	)
	event = models.ForeignKey(
		Event,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="event"
	)

	def __str__(self):
		return self.name
	
class Chat(models.Model):
	name = models.CharField(max_length=24)

	def __str__(self):
		return self.name

class Message(models.Model):
	text = models.CharField(
		max_length=255,
	)
	sender = models.ForeignKey(
		Friend,
		blank=False,
		null=False,
		related_name="sent_messages",
		on_delete=models.CASCADE,
	)
	chat = models.ForeignKey(
		Chat,
		on_delete=models.CASCADE,
		related_name="messages"
	)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.text
	
class Carpool(models.Model):
	event = models.ForeignKey(
		Event,
		on_delete=models.CASCADE,
		related_name="carpools"
	)
	driver = models.ForeignKey(
		Friend,
		on_delete=models.CASCADE,
		related_name="driver_carpools"
	)
	seats = models.PositiveIntegerField(default=4)

	def __str__(self):
		return f"{self.driver.name}'s car for {self.event.name}"
	
class CarpoolRider(models.Model):
	carpool = models.ForeignKey(
		Carpool,
		on_delete=models.CASCADE,
		related_name="riders"
	)
	friend = models.ForeignKey(
		Friend,
		on_delete=models.CASCADE,
		related_name="carpool_riders"
	)

	class Meta:
		unique_together = ("carpool", "friend")

	def __str__(self):
		return f"{self.friend.name} in {self.carpool}"