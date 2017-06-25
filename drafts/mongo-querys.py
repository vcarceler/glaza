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
    print("Documents with MAC 94:de:80:d1:64:0d")
    result = COLLECTION.find({"ansible_facts.ansible_default_ipv4.macaddress": "94:de:80:d1:64:0d"})
    show(result)
    print()


def show(cursor):
    """Shows cursor's contents."""

    for doc in cursor:
        print(doc)

    print("\n")



querys()
