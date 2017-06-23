from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import Network

# Create your views here.
def index(request):
    """Shows list of networks."""

    network_list = Network.objects.all()
    context = {'network_list': network_list}

    return render(request, 'ui/index.html', context)

def network(request, network_id):
    """Shows a network."""

    # network = Network.objects.get(name=network_id)
    # return HttpResponse("You're looking at network %s." % network.address)

    return render(request, 'ui/test-template.html', context=None)

def host(request, host_id):
    """Shows host's details."""

    return HttpResponse("You're looking at host %s." % host_id)
