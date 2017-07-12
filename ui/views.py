from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .models import Network

from util.mongo import get_network_cpu_report, get_network_memory_report, get_network_disk_report, get_network_vendor_report, get_network_hostcount, get_network_details, get_host

from pprint import pprint
from operator import itemgetter


# Create your views here.
def index(request):
    """Redirect to first network."""

    network_list = Network.objects.all().order_by('name')

    return redirect('/network/{}'.format(network_list[0].name))

def network(request, network_id):
    """Shows a network."""

    network_queryset = Network.objects.filter(name=network_id)
    current_network = network_queryset[0]

    network_list = Network.objects.all().order_by('name')
    
    cpu_report = get_network_cpu_report(current_network.address)
    memory_report = get_network_memory_report(current_network.address)
    disk_report = get_network_disk_report(current_network.address)
    vendor_report = get_network_vendor_report(current_network.address)
    host_count = get_network_hostcount(current_network.address)
    network_details = get_network_details(current_network.address)

    context = {
        'current_network': current_network,
        'network_list': network_list,
        'cpu_report': cpu_report,
        'memory_report': memory_report,
        'disk_report': disk_report,
        'vendor_report': vendor_report,
        'host_count': host_count,
        'network_details': network_details,
        }

    return render(request, 'ui/network.html', context)

def host(request, host_id):
    """Shows host's details."""

    network_list = Network.objects.all().order_by('name')

    host = get_host(host_id)

    context = {
        'host_id': host_id,
        'network_list': network_list,
        'host': host,
    }

    return render(request, 'ui/host.html', context)
