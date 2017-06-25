from pymongo import MongoClient

client = MongoClient()
database = client.glaza
collection = database.facts

# Get unique macaddresses
result = collection.distinct( "ansible_facts.ansible_default_ipv4.macaddress" )
print(result)

# Get last JSON of a macaddress
result = collection.find( "ansible_facts.ansible_default_ipv4.macaddress": "94:de:80:d1:64:0d" )
print(result)
