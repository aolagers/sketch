from django.db import models
import datetime


class Drawing(models.Model):

  image = models.ImageField(upload_to="drawings/")
  created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return str(self.pk)

  def humanize_timediff(self):
    delta = datetime.datetime.now() - self.created
    human_date = ""

    if delta.days > 6:
      human_date =  self.created.strftime("%j.%n.%Y %H:%i")
    elif delta.days > 2:
      human_date =  self.created.strftime("last %A %H:%i")
    elif delta.days == 1:
      human_date =  "yesterday at %H:%i"
    elif delta.seconds > 7200:
      human_date =  str(delta.seconds / 3600) + " hours ago"
    elif delta.seconds > 120:
      human_date =  str(delta.seconds / 60) + " minutes ago"
    else:
      human_date =  "a few seconds ago"
    return human_date
      
