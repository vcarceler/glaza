from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /host/1c:c1:de:50:21:12/
    url(r'^(?P<host_id>([[0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))/$', views.host, name='host'),
]