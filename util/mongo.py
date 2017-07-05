import json
from pymongo import MongoClient
from pprint import pprint

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
    json_string = ansible_output.replace("vt.handoff", "vt_handoff").replace("intel_idle.max_cstate", "intel_idle_max_cstate")

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

def get_network_cpu_report(network_address: str):
    """Return a dictionary with the cpu report."""

    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
        {"$group": {"_id": "$ansible_facts.ansible_processor", "count": {"$sum": 1}}},
    ])

    cpu_dictionary = {}
    for element in result:
        cpu_id = element['_id'][1]
        count = element['count']
        cpu_dictionary[cpu_id] = count

    return cpu_dictionary


def get_network_memory_report(network_address: str):
    """Return a dictionary with the memory report."""

    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
        {"$group": {"_id": "$ansible_facts.ansible_memtotal_mb", "count": {"$sum": 1}}},
    ])

    memory_dictionary = {}
    for element in result:
        key = element['_id']
        count = element['count']
        memory_dictionary[key] = count

    return memory_dictionary

def get_network_disk_report(network_address: str):
    """Return a dictionary with the disk report."""

    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
        {"$group": {"_id": "$ansible_facts.ansible_devices.sda.size", "count": {"$sum": 1}}},
    ])

    disk_dictionary = {}
    for element in result:
        key = element['_id']
        count = element['count']
        disk_dictionary[key] = count

    return disk_dictionary

def get_network_vendor_report(network_address: str):
    """Return a dictionary with the system vendor report."""

    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
        {"$group": {"_id": "$ansible_facts.ansible_system_vendor", "count": {"$sum": 1}}},
    ])

    vendor_dictionary = {}
    for element in result:
        key = element['_id']
        count = element['count']
        vendor_dictionary[key] = count

    return vendor_dictionary

def get_network_hostcount(network_address: str):
    """Return the number of hosts in the network."""

    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(network_address)}},
        {"$group": {"_id": "$ansible_facts.ansible_default_ipv4.macaddress", "count": {"$sum": 1}}},
    ])

    count = 0
    for element in result:
        count = count + 1

    return count

def get_network_details(network_address: str):
    """Return a dictionary with the list of hosts."""

    result = COLLECTION.aggregate([
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
    ])

    hosts = []
    for element in result:
        ansible_facts = element['ansible_facts']
        ansible_facts['ansible_processor'] = ansible_facts['ansible_processor'][1]
        hosts.append(ansible_facts)

    return hosts

def get_host(host_id: str):
    """Return the especified host (by MAC)."""

    pprint("host_id: {}".format(host_id))
    result = COLLECTION.find_one({"ansible_facts.ansible_default_ipv4.macaddress": host_id})

    pprint(result)

    return result
