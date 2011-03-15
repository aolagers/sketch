from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from paste.models import Sketch

def new_sketch(request):
  """Shows the drawing canvas. If "sketch_id" in GET data, shows the sketch instead."""
  if request.GET.get("sketch_id"):
    return redirect("/" + request.GET.get("sketch_id"))
  return render_to_response("new.html", RequestContext(request))

def delete_sketch(request, sketch_id):
  try:
    sketch = Sketch.objects.get(pk=sketch_id)
    if sketch.image:
      sketch.image.delete()
    sketch.delete()
  except Sketch.DoesNotExist:
    sketch = None;

  messages.error(request, "sketch deleted")
  return redirect("/browse/")

def show_sketch(request, sketch_id):
  try:
    sketch = Sketch.objects.get(pk=sketch_id)
  except Sketch.DoesNotExist:
    sketch = None;
  except ValueError:
    sketch = None;

  return render_to_response("show_sketch.html", RequestContext(request, {"sketch": sketch}))


def browse(request):
  """A paginated view for browsing all sketches."""
  sketches_all = Sketch.objects.all().order_by("-created")
  paginator = Paginator(sketches_all, 9)

  try:
    page = int(request.GET.get('page', '1'))
  except ValueError:
    page = 1

  try:
    sketches = paginator.page(page)
  except (EmptyPage, InvalidPage):
    sketches = paginator.page(paginator.num_pages)
    
  return render_to_response("browse.html", RequestContext(request, {"pages": sketches}))

import base64
def save_sketch(request):
  """Saves a png sketch to the database.
  Input:
    a json object {"img":data} where data is a base64 encoded png.
  Output:
    a json object {"sketch_id":id} where id is the primary key of the saved object.
  """
  print "saving"
  if request.method == "POST" and request.is_ajax():
    print "is_ajax"
    imgstring = str(request.POST.get("img"))
    pngstring = base64.b64decode(imgstring.split(",")[1])
    new_sketch = Sketch()
    new_sketch.save()
    new_sketch.image.save(str(new_sketch.pk) + ".png", ContentFile(pngstring))
    json = '{"sketch_id" : "%s"}' % new_sketch.pk
    print json
    messages.success(request, "successfully posted a new sketch!")
    return HttpResponse(json, mimetype="application/json")

  return HttpResponseNotFound("invalid save request")

