""" django views.py """
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import base64

from paste.models import Sketch

def new_sketch(request):
    """Shows the drawing canvas.
    If "sketch_id" in GET data, shows the sketch instead."""
    
    t = request.GET.get("t")
    if t == "light" or t == "dark":
        request.session["theme"] = t + ".css"
        return redirect(request.META.get("HTTP_REFERER"))

    if request.GET.get("sketch_id"):
        sketch = Sketch.objects.get(pk = request.GET.get("sketch_id"))
        return redirect(sketch)
    return render_to_response("new.html", RequestContext(request))

def delete_sketch(request, sketch_id):
    """ Deletes a sketch and the associated image. """
    try:
        sketch = Sketch.objects.get(pk=sketch_id)
        if sketch.image:
            sketch.image.delete()
        sketch.delete()
    except Sketch.DoesNotExist:
        pass

    messages.error(request, "sketch deleted")
    return redirect("/browse/")

def show_sketch(request, sketch_id):
    """ Fetches one sketch and renders it. """
    try:
        sketch = Sketch.objects.get(pk=sketch_id)
    except (ValueError, Sketch.DoesNotExist):
        sketch = None

    return render_to_response("show_sketch.html",
            RequestContext(request, {"sketch" : sketch}))


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
        
    return render_to_response("browse.html",
            RequestContext(request, {"pages" : sketches}))

def about(request):
    """ Shows random site info. """
    count = Sketch.objects.all().count()
    return render_to_response("about.html",
            RequestContext(request, {"count" : count}))

def save_sketch(request):
    """Saves a png sketch to the database.
    Input:
    a json object {"img":data} where data is a base64 encoded png.
    Output:
    a json object {"sketch_id":id} where id is the primary key of the saved object.
    """
    if request.method == "POST" and request.is_ajax():
        imgstring = str(request.POST.get("img"))
        pngstring = base64.b64decode(imgstring.split(",")[1])
        sketch = Sketch()
        sketch.save()
        sketch.image.save(str(sketch.pk) + ".png", ContentFile(pngstring))
        json = '{"sketch_id" : "%s"}' % sketch.pk
        print "new image: %s" % json
        messages.success(request, "successfully posted a new sketch!")
        return HttpResponse(json, mimetype="application/json")

    return HttpResponseNotFound("invalid save request")

