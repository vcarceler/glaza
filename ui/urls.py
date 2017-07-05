from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /network/Torvalds/
    url(r'^(?P<network_id>[a-zA-Z0-9\-_]+)/$', views.network, name='network'),
    # ex: /network/5/
    #url(r'^(?P<host_id>[0-9:abcdef]+)/$', views.host, name='host'),
]