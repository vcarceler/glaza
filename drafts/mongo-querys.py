from pymongo import MongoClient

CLIENT = MongoClient()
DATABASE = CLIENT.glaza
COLLECTION = DATABASE.facts

def querys():
    """Executes sample mongo querys."""

    # Get all documents
    # result = COLLECTION.find({})
    # show(result)

    # Get unique macaddresses
    print("Different MAC addresses:")
    result = COLLECTION.distinct("ansible_facts.ansible_default_ipv4.macaddress")
    print(result)
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
        }).sort("ansible_facts.ansible_date_time.iso8601", -1)
    show(result)
    print()

    NETWORK = "192.168.100.0"

    # Count cpu's types from a network
    print("Aggregated CPUs of network {}".format(NETWORK))
    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(NETWORK)}},
        {"$group": {"_id": "$ansible_facts.ansible_processor", "count": {"$sum": 1}}},
    ])
    show(result)
    print()

    # Count RAM size from a network
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

    # Get only last version of every host in network...
    # It's a two phases aproach
    # a) count how many different machines -> n
    # b) match, sort and limit to "n"
    print("Last version of every host in a network...")

    print(" -> How many diferents hosts in network?")
    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(NETWORK)}},
        {"$group": {"_id": "$ansible_facts.ansible_default_ipv4.macaddress", "count": {"$sum": 1}}},
    ])

    # Count the number of MACs
    n = 0
    for doc in result:
        n = n + 1

    
    print(" -> Ok, {}, then...".format(n))
    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(NETWORK)}},
        {"$sort": {"ansible_facts.ansible_date_time.iso8601": -1}},
        {"$limit": n},
        #{"$group": {"_id": "$ansible_facts.ansible_default_ipv4.macaddress", "count": {"$sum": 1}}},
        # {"$group": {"_id": "$ansible_facts.ansible_memtotal_mb", "count": {"$sum": 1}}},
        {"$project": {"ansible_facts.ansible_date_time.iso8601": 1, "ansible_facts.ansible_default_ipv4.macaddress": 1}},
    ])
    show(result)
    print()

    # And finally count memory of every host in a network without considering old samples.
    print("Shows memory report for a network without considering old samples.")
    result = COLLECTION.aggregate([
        {"$match": {"ansible_facts.ansible_default_ipv4.network": "{}".format(NETWORK)}},
        {"$sort": {"ansible_facts.ansible_date_time.iso8601": -1}},
        {"$limit": n},
        {"$group": {"_id": "$ansible_facts.ansible_memtotal_mb", "count": {"$sum": 1}}},
    ])
    show(result)
    print()


def show(cursor):
    """Shows cursor's contents."""

    for doc in cursor:
        print(doc)

    print("\n")



querys()
