from django.contrib import admin
from models import Sketch



class SketchAdmin(admin.ModelAdmin):
    #fields = ('image', 'thumbnail')
    list_display = ('key', 'created', 'thumbnail')
    date_hierarchy = 'created'

admin.site.register(Sketch, SketchAdmin)

