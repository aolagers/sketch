from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def front(request):
  if request.GET.get("id"):
    return redirect("/" + request.GET.get("id"))

  return render_to_response("front.html", RequestContext(request))

def show_sketch(request, sketch_id):
  return render_to_response("show_sketch.html", RequestContext(request, {"sketch_id": sketch_id}))

