from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.core.files.base import ContentFile

from paste.models import Drawing

def front(request):
  if request.GET.get("sketch_id"):
    return redirect("/" + request.GET.get("id"))

  return render_to_response("front.html", RequestContext(request))

def show_sketch(request, sketch_id):
  try:
    sketch = Drawing.objects.get(pk=sketch_id)
  except Drawing.DoesNotExist:
    sketch = None;
  return render_to_response("show_sketch.html", RequestContext(request, {"sketch": sketch}))

import base64
def save_sketch(request):
  if request.method == "POST" and request.is_ajax():
    imgstring = str(request.POST.get("img"))
    f = base64.b64decode(imgstring.split(",")[1])
    print f
    d = Drawing()
    d.save()
    #stringio = StringIO.StringIO(imgstring)
    c = ContentFile(f)
    d.image.save(str(d.pk) + ".png", c)
    


    return HttpResponse(d.pk)
  elif request.GET.get("sketch-id"):
    sid = request.GET.get("sketch-id")
    return redirect("/%s/"%sid)

  return HttpResponseNotFound()
