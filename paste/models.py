from django.db import models

class Drawing(models.Model):
  image = models.ImageField(upload_to="drawings/")
  created = models.DateTimeField(auto_now=True)

