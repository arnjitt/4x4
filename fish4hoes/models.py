from django.db import models

class Event(models.Model):
	name = models.CharField(max_length=200)

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
	
