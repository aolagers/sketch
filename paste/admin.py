from django.contrib import admin
from paste.models import Drawing

class SketchAdmin(admin.ModelAdmin):
  #fields = ('image', 'created')
  list_display = ('key', 'created',)
  date_hierarchy = 'created'

admin.site.register(Drawing, SketchAdmin)

