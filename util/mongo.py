import json
from pymongo import MongoClient
from pprint import pprint
from operator import itemgetter

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
    json_string = json_string.replace("intel_idle.max_cstate", "intel_idle_max_cstate")


    try:

        while 1:
            first_key = json_string.index('SUCCESS =>')
            substring = json_string[first_key+10:]
            last_key = substring.find('\n}')
            js1_string = substring[:last_key+2]

            data = json.loads(js1_string)

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

def replace_jsons(ansible_output: str):
    """Replaces documents if they exists, if not just inserts.

    Return number of processed (replaced or inserted) jsons.
    A replacement occurs when exists a document with same MAC."""

    count = 0

    json_list = parse_ansible_output(ansible_output)
    for document in json_list:
        COLLECTION.delete_many(
            {"ansible_facts.ansible_default_ipv4.macaddress": "{}".format(document['ansible_facts']['ansible_default_ipv4']['macaddress'])}
        )
        COLLECTION.insert(document)
        count = count + 1

    return count

def get_cpu_report(network_address="0.0.0.0"):
    """Return a list of (cpu, count) reverse sorted by count for the specified network_address.
    
    Just use network_address="0.0.0.0" to get a report of all hosts."""

    if network_address == "0.0.0.0":
        mongo_query = [
            {"$group": {"_id": "$ansible_facts.ansible_processor", "count": {"$sum": 1}}},
            ]
    else:
        mongo_query = [
            {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
            {"$group": {"_id": "$ansible_facts.ansible_processor", "count": {"$sum": 1}}},
            ]

    result = COLLECTION.aggregate(mongo_query)

    cpu_dictionary = {}
    for element in result:
        cpu_id = element['_id'][1]
        count = element['count']
        cpu_dictionary[cpu_id] = count

    return sorted(cpu_dictionary.items(), key=itemgetter(1), reverse=True)


def get_memory_report(network_address="0.0.0.0"):
    """Return a list (ram, count) reverse sorted by count for the specified network_address.
    
    Just use network_address="0.0.0.0" to get a report of all hosts."""

    if network_address == "0.0.0.0":
        mongo_query = [
            {"$group": {"_id": "$ansible_facts.ansible_memtotal_mb", "count": {"$sum": 1}}},
            ]
    else:
        mongo_query = [
            {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
            {"$group": {"_id": "$ansible_facts.ansible_memtotal_mb", "count": {"$sum": 1}}},
            ]

    result = COLLECTION.aggregate(mongo_query)

    memory_dictionary = {}
    for element in result:
        key = element['_id']
        count = element['count']
        memory_dictionary[key] = count

    return sorted(memory_dictionary.items(), key=itemgetter(1), reverse=True)

def get_disk_report(network_address="0.0.0.0"):
    """Return a list (disk, count) reverse sorted by count for the specified network_address.
    
    Just use network_address="0.0.0.0" to get a report of all hosts."""

    if network_address == "0.0.0.0":
        mongo_query = [
            {"$group": {"_id": "$ansible_facts.ansible_devices.sda.size", "count": {"$sum": 1}}},
        ]
    else:
        mongo_query = [
            {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
            {"$group": {"_id": "$ansible_facts.ansible_devices.sda.size", "count": {"$sum": 1}}},
        ]

    result = COLLECTION.aggregate(mongo_query)

    disk_dictionary = {}
    for element in result:
        key = element['_id']
        count = element['count']
        disk_dictionary[key] = count

    return sorted(disk_dictionary.items(), key=itemgetter(1), reverse=True)

def get_vendor_report(network_address="0.0.0.0"):
    """Return a list (vendor, count) reverse sorted by count for the specified network_address.
    
    Just use network_address="0.0.0.0" to get a report of all hosts."""

    if network_address == "0.0.0.0":
        mongo_query = [
            {"$group": {"_id": "$ansible_facts.ansible_system_vendor", "count": {"$sum": 1}}},
        ]
    else:
        mongo_query = [
            {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
            {"$group": {"_id": "$ansible_facts.ansible_system_vendor", "count": {"$sum": 1}}},
        ]

    result = COLLECTION.aggregate(mongo_query)

    vendor_dictionary = {}
    for element in result:
        key = element['_id']
        count = element['count']
        vendor_dictionary[key] = count

    return sorted(vendor_dictionary.items(), key=itemgetter(1), reverse=True)

def get_hostcount(network_address="0.0.0.0"):
    """Return host count for the specified network_address.
    
    Just use network_address="0.0.0.0" to get a report of all hosts."""

    if network_address == "0.0.0.0":
        mongo_query = [
            {"$group": {"_id": "$ansible_facts.ansible_default_ipv4.macaddress", "count": {"$sum": 1}}},
        ]
    else:
        mongo_query = [
            {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
            {"$group": {"_id": "$ansible_facts.ansible_default_ipv4.macaddress", "count": {"$sum": 1}}},
        ]

    result = COLLECTION.aggregate(mongo_query)

    count = 0
    for element in result:
        count = count + 1

    return count

def get_hosts(network_address="0.0.0.0"):
    """Return a list of hosts with some facts for the specified network_address.
    
    Just use network_address="0.0.0.0" to get a report of all hosts."""

    if network_address == "0.0.0.0":
        mongo_query = [
            {"$project": {
                "ansible_facts.ansible_hostname": 1,
                "ansible_facts.ansible_default_ipv4.address": 1,
                "ansible_facts.ansible_default_ipv4.macaddress": 1,
                "ansible_facts.ansible_processor": 1,
                "ansible_facts.ansible_processor_vcpus": 1,
                "ansible_facts.ansible_memtotal_mb": 1,
                "ansible_facts.ansible_devices.sda.size": 1,
                "ansible_facts.ansible_lsb.description": 1,
                "ansible_facts.ansible_kernel": 1,
                "ansible_facts.ansible_system_vendor": 1,
                "ansible_facts.ansible_date_time.date": 1,
                "ansible_facts.ansible_date_time.time": 1,
                }},
        ]
    else:
        mongo_query = [
            {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
            {"$project": {
                "ansible_facts.ansible_hostname": 1,
                "ansible_facts.ansible_default_ipv4.address": 1,
                "ansible_facts.ansible_default_ipv4.macaddress": 1,
                "ansible_facts.ansible_processor": 1,
                "ansible_facts.ansible_processor_vcpus": 1,
                "ansible_facts.ansible_memtotal_mb": 1,
                "ansible_facts.ansible_devices.sda.size": 1,
                "ansible_facts.ansible_lsb.description": 1,
                "ansible_facts.ansible_kernel": 1,
                "ansible_facts.ansible_system_vendor": 1,
                "ansible_facts.ansible_date_time.date": 1,
                "ansible_facts.ansible_date_time.time": 1,
                }},
        ]

    result = COLLECTION.aggregate(mongo_query)

    hosts = []
    for element in result:
        ansible_facts = element['ansible_facts']
        ansible_facts['ansible_processor'] = ansible_facts['ansible_processor'][1]
        hosts.append(ansible_facts)

    return hosts

def get_host(host_id: str):
    """Return the especified host (by MAC)."""

    result = COLLECTION.find_one({"ansible_facts.ansible_default_ipv4.macaddress": host_id})

    return result
