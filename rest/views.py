import json
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pymongo import MongoClient
from util.mongo import insert_jsons, replace_jsons


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    """Stores JSON data in mongodb."""

    result = ""

    if request.method == 'POST':
        count = replace_jsons(str(request.body.decode()))
        result = 'Hosts registered: {}'.format(count)


    elif request.method == 'GET':
        result = "Глаза REST API: \
        Send json data: curl -X POST --data-binary @ansible_output_file http://127.0.0.1:8000/rest/"


    return HttpResponse(result)

