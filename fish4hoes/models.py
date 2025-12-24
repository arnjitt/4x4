from django.db import models

class Friend(models.Model):
  name = models.CharField(max_length=100)

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