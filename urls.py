from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from paste.views import front, showsketch

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^draw/', include('draw.foo.urls')),

    (r'^$', front),
    (r'^(\w+)$', showsketch),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
