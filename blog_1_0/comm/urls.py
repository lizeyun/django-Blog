from django.conf.urls import include, url
from views import index, comm



urlpatterns = [
    # Examples:
    # url(r'^$', 'dj_blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', index),
    url(r'^ar/(?P<post_id>\d+)$', comm)

]
