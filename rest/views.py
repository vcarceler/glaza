import json
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pymongo import MongoClient


# Create your views here.
@api_view(['GET', 'POST'])
def index(request):
    """Stores JSON data in mongodb."""

    result = ""

    if request.method == 'POST':
        json_string = request.POST['json'].replace("vt.handoff", "vt_handoff")
        count = 0

        try:
            client = MongoClient()
            database = client.glaza
            collection = database.facts

            while 1:
                first_key = json_string.index('SUCCESS =>')
                substring = json_string[first_key+10:]
                #result = '{} SUBSTRING: {}'.format(result, substring)
                last_key = substring.find('\n}')
                #result = '{} LAST_KEY: {}'.format(result, last_key)
                js1_string = substring[:last_key+2]
                result = '{} JS1={}'.format(result, js1_string)

                data = json.loads(js1_string)

                collection.insert(data)
                count = count + 1

                json_string = substring[last_key:]
        except:
            pass

        result = '{} {} documentos registrados'.format(result, count)


    elif request.method == 'GET':
        result = 'Глаза REST API: \
        Send json data: curl -X POST --data "json=$data" http://IP/rest/'

    return HttpResponse(result)
