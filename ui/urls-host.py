from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /host/5/
    url(r'^(?P<host_id>[0-9]+)/$', views.host, name='host'),
]