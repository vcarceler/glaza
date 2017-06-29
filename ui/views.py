from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import Network

from pymongo import MongoClient


# Create your views here.
def index(request):
    """Shows list of networks."""

    network_list = Network.objects.all()
    context = {'network_list': network_list}

    return render(request, 'ui/index.html', context)

def network(request, network_id):
    """Shows a network."""

    print("network_id: {}".format(network_id))

    # network = Network.objects.get(name=network_id)
    # return HttpResponse("You're looking at network %s." % network.address)

    client = MongoClient()
    database = client.glaza
    collection = database.facts
    
    network_list = Network.objects.all()
    context = {
        'network_id': network_id,
        'network_list': network_list,
        }

    return render(request, 'ui/network.html', context)

def host(request, host_id):
    """Shows host's details."""

    return HttpResponse("You're looking at host %s." % host_id)
