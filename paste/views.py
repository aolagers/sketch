from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.base import ContentFile

from paste.models import Drawing

def front(request):
  if request.GET.get("sketch_id"):
    return redirect("/" + request.GET.get("sketch_id"))
  return render_to_response("front.html", RequestContext(request))

def delete_sketch(request, sketch_id):
  try:
    sketch = Drawing.objects.get(pk=sketch_id)
    if sketch.image:
      sketch.image.delete()
    sketch.delete()
  except Drawing.DoesNotExist:
    sketch = None;

  messages.error(request, "sketch deleted")
  return redirect("/all")

def show_sketch(request, sketch_id):
  try:
    sketch = Drawing.objects.get(pk=sketch_id)
  except Drawing.DoesNotExist:
    sketch = None;
  except ValueError:
    sketch = None;

  return render_to_response("show_sketch.html", RequestContext(request, {"sketch": sketch}))

def show_latest(request):
  n = 9
  sketches = Drawing.objects.all().order_by("-created")[:n]
  return render_to_response("show_all.html", RequestContext(request, {"sketches": sketches, "sketch_count": n}))

from django.core.paginator import Paginator
def show_all(request):
  sketches_all = Drawing.objects.all().order_by("-created")
  paginator = Paginator(sketches_all, 9)
  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    sketches = paginator.page(page)
  except:
    sketches = paginator.page(paginator.num_pages)
    
  return render_to_response("show_all.html", RequestContext(request, {"sketches": sketches}))

import base64
def save_sketch(request):
  if request.method == "POST" and request.is_ajax():
    imgstring = str(request.POST.get("img"))
    pngstring = base64.b64decode(imgstring.split(",")[1])
    new_drawing = Drawing()
    new_drawing.save()
    new_drawing.image.save(str(new_drawing.pk) + ".png", ContentFile(pngstring))
    json = '{"sketch_id" : "%s"}' % new_drawing.pk
    print json
    messages.success(request, "successfully posted a new sketch!")
    return HttpResponse(json, mimetype="application/json")

  return HttpResponseNotFound("invalid save request")

