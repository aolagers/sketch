from django.conf.urls.defaults import patterns, include
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

from sketch import views

urlpatterns = patterns('',

    (r'^$', views.index),

    (r'^save/$', views.save_sketch),
    #(r'^test/$', 'django.views.generic.simple.direct_to_template', {"template":"test.html"}),
    (r'^browse/$', views.browse),
    (r'^about/$', views.about),
    (r'^delete/(\w+)/$', views.delete_sketch),

    (r'^admin/', include(admin.site.urls)),

    #(r'^static/(?P<path>.*)$', 'django.views.static.serve', {"document_root": settings.MEDIA_ROOT}),

    (r'^(\w+)/$', views.show_sketch),


    #(r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/favicon.ico'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
