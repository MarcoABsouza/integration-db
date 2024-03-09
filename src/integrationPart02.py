import datetime
import pprint
import pymongo as pyM

client = pyM.MongoClient("SET here your link give by mongodb atlas")

data_bank = client.test
collection = data_bank.test_collection

print(data_bank.test_collection)

client_id = collection.find_one(sort=[("id", pyM.DESCENDING)])
id = client_id["id"] + 1 if client_id else 1

client_01 = {
    "id": id,
    "name": "Marco Aurelio",
    "cpf": "12345678912",
    "address": "goiania/Go",
    "accounts": [
        {
            "type_account": "Current account",
            "agency": "0001",
            "number_account": "123456",
            "balance": 1000,
            "tags": ["current account", "bank account", "client 01"],
            "date": datetime.datetime.now(datetime.UTC),
        },
        {
            "type_account": "savings account",
            "agency": "0002",
            "number_account": "123457",
            "balance": 100,
            "tags": ["savings account", "bank account", "client 01"],
            "date": datetime.datetime.now(datetime.UTC),
        },
    ],
}

collection.insert_one(client_01)


def search_and_print_clients():
    """Searches and prints client and account information from the collection."""
    clients = collection.find()
    for client in clients:
        print(f"Client: {client['name']}")
        for account in client["accounts"]:
            print(
                f"\t- Account: {account['type_account']} ({account['number_account']})"
            )


search_and_print_clients()
