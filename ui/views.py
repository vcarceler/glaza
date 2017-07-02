from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from .models import Network

from util.mongo import get_network_cpu_report, get_network_memory_report, get_network_disk_report, get_network_vendor_report

from pprint import pprint


# Create your views here.
def index(request):
    """Shows list of networks."""

    network_list = Network.objects.all()
    context = {'network_list': network_list}

    return render(request, 'ui/index.html', context)

def network(request, network_id):
    """Shows a network."""

    network_queryset = Network.objects.filter(name=network_id)
    current_network = network_queryset[0]

    network_list = Network.objects.all()
    
    cpu_report = get_network_cpu_report(current_network.address)
    memory_report = get_network_memory_report(current_network.address)
    disk_report = get_network_disk_report(current_network.address)
    vendor_report = get_network_vendor_report(current_network.address)

    context = {
        'current_network': current_network,
        'network_list': network_list,
        'cpu_report': cpu_report,
        'memory_report': memory_report,
        'disk_report': disk_report,
        'vendor_report': vendor_report,
        }

    return render(request, 'ui/network.bootstrap.dashboard.html', context)

def host(request, host_id):
    """Shows host's details."""

    return HttpResponse("You're looking at host %s." % host_id)
