from django.db import models

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

  def __str__(self):
    return self.name
  
class Event(models.Model):
  eventName = models.CharField(max_length=200)
  hostName = models.ForeignKey(
    Friend, 
    on_delete=models.CASCADE,
    related_name="hosted_events"
    )
  
  def __str__(self):
    return self.eventName