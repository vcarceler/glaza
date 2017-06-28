from pymongo import MongoClient

CLIENT = MongoClient()
DATABASE = CLIENT.glaza
COLLECTION = DATABASE.facts

def querys():
    """Executes test mongo querys."""

    # Get all documents
    # result = COLLECTION.find({})
    # show(result)

    # Get unique macaddresses
    print("Different MAC addresses:")
    result = COLLECTION.distinct("ansible_facts.ansible_default_ipv4.macaddress")
    print(result)
    print()

    # Get last JSON of a macaddress
    print("Documents with MAC 1c:c1:de:50:21:12")
    result = COLLECTION.find({"ansible_facts.ansible_default_ipv4.macaddress": "1c:c1:de:50:21:12"})
    show(result)
    print()

    # Get specified fields
    print("especified fields of 1c:c1:de:50:21:12")
    result = COLLECTION.find(
        {"ansible_facts.ansible_default_ipv4.macaddress": "1c:c1:de:50:21:12"},
        {
            "ansible_facts.ansible_default_ipv4.macaddress": "1",
            "ansible_facts.ansible_date_time.iso8601": "1",
            "ansible_facts.ansible_devices.sda.size": "1",
            "ansible_facts.ansible_system_vendor": "1",
        })
    show(result)
    print()

    # Count RAM size from a network
    NETWORK = "192.168.17.0"
    print("Aggregated RAM of network {}".format(NETWORK))
    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(NETWORK)}},
        {"$group": {"_id": "$ansible_facts.ansible_memtotal_mb", "count": {"$sum": 1}}},
    ])
    show(result)
    print()

    # Count DISK size from a network
    print("Aggregated DISK of network {}".format(NETWORK))
    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(NETWORK)}},
        {"$group": {"_id": "$ansible_facts.ansible_devices.sda.size", "count": {"$sum": 1}}},
    ])
    show(result)
    print()


def show(cursor):
    """Shows cursor's contents."""

    for doc in cursor:
        print(doc)

    print("\n")



querys()
