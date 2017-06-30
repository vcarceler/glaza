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
        result = '{} {} documentos registrados'.format(result, count)


    elif request.method == 'GET':
        result = "Глаза REST API: \
        Send json data: curl -X POST --data-binary @<ansible's output's file> http://127.0.0.1:8000/rest/"


    return HttpResponse(result)

# @api_view(['GET', 'POST'])
# def postansibleoutputfile(request):
#     """Stores JSON data in mongodb.
#     Receives json file: curl -X POST --data-binary "@dpt-inf.ansible_output" http://127.0.0.1:8000/rest/v2/"""

#     result = ""
#     json_string = str(request.body.decode())
#     #result = "Received data: {}\n\n".format(json_string)
#     json_string = json_string.replace("vt.handoff", "vt_handoff")
#     #result = "{}\n\njson_string replaced: {}\n\n".format(result, json_string)
    

#     count = 0

#     try:
#         client = MongoClient()
#         database = client.glaza
#         collection = database.facts

#         while 1:
#             first_key = json_string.index('SUCCESS =>')
#             substring = json_string[first_key+10:]
#             #result = '\n\n{} SUBSTRING: {}\n\n'.format(result, substring)
#             last_key = substring.find('\n}')
#             #result = '\n\n{} LAST_KEY: {}\n\n'.format(result, last_key)
#             js1_string = substring[:last_key+2]
#             #result = '\n\n{} JS1={}\n\n'.format(result, js1_string)

#             data = json.loads(js1_string)

#             collection.insert(data)
#             count = count + 1

#             json_string = substring[last_key:]
#     except:
#         pass

#     result = '{} {} documentos registrados'.format(result, count)

#     return HttpResponse(result)

