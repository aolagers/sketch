from django.conf.urls.defaults import patterns, include
from django.views.generic.simple import direct_to_template
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from paste import views

urlpatterns = patterns('',
    # Example:
    # (r'^draw/', include('draw.foo.urls')),

    (r'^$', views.front),
    (r'^save/$', views.save_sketch),
    (r'^all/$', views.show_all),
    (r'^latest/$', views.show_latest),
    (r'^(\w+)/$', views.show_sketch),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {"document_root": settings.MEDIA_ROOT})
)
