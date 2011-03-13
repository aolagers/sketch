# Create your views here.

from django.shortcuts import render_to_response, redirect

def front(request):
  if "id" in request.GET and request.GET["id"]:
    return redirect("/" + request.GET["id"])

  return render_to_response("front.html")

def showsketch(request, id):
  return render_to_response("sketch.html", {"id": id})

