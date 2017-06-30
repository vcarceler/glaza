import json
from pymongo import MongoClient

CLIENT = MongoClient()
DB = CLIENT.glaza
COLLECTION = DB.facts

def query():
    '''Prints MAC addresses.'''

    print("Different MAC addresses:")
    result = COLLECTION.distinct("ansible_facts.ansible_default_ipv4.macaddress")
    print(result)
    print()


def parse_ansible_output(ansible_output: str):
    '''Return a list with JSONs extracted from ansible's output.'''

    json_list = []
    json_string = ansible_output.replace("vt.handoff", "vt_handoff")

    try:

        while 1:
            first_key = json_string.index('SUCCESS =>')
            substring = json_string[first_key+10:]
            last_key = substring.find('\n}')
            js1_string = substring[:last_key+2]

            data = json.loads(js1_string)

            #print(data['ansible_facts']['ansible_default_ipv4']['macaddress'])

            # Insert the document
            json_list.append(data)

            json_string = substring[last_key:]

    except:
        pass

    return json_list

def insert_jsons(ansible_output: str):
    """Insert Ansible's output into MongoDB's collection.

    Return number of inserted jsons."""

    count = 0
    json_list = parse_ansible_output(ansible_output)
    for document in json_list:
        COLLECTION.insert(document)
        count = count + 1

    return count
