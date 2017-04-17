from django.conf.urls import include, url
from django.contrib import admin
from views import test, article
import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^test/$', test),
    url(r'^article/$', article),
    url(r'^comm/', include('comm.urls')),
    url(r'^media/article/(?P<path>.*)', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT+'/article'}),
]
