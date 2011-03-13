# Create your views here.

from django.shortcuts import render_to_response, redirect

def front(request):
  if request.GET.get("id"):
    return redirect("/" + request.GET.get("id"))

  return render_to_response("front.html")

def show_sketch(request, sketch_id):
  return render_to_response("show_sketch.html", {"sketch_id": sketch_id})

