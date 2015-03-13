from django.conf.urls import patterns, url, include
from django.conf import settings
from django.contrib import admin

from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^superadmin/', include(admin.site.urls)),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^robots\.txt$', include('robots.urls')),
    url(r'', include('bonfire.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    from django.conf.urls.static import static

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
