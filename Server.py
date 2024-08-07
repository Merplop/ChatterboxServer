from enum import Enum
import threading
import pymongo
from fastapi import FastAPI
from pymongo import MongoClient
import asyncio
from websockets.server import serve
from Request import Request
from colorama import Fore
from datetime import date, datetime
import os

queue = []
app = FastAPI()
app.mongodb_client = None
app.database = None


def get_database():
    CONNECTION_STRING = "mongodb+srv://mirohaapalainen:05xiHzhyngidFSW7@chattercluster.ljuhfn2.mongodb.net/?retryWrites=true&w=majority&appName=ChatterCluster"
    client = MongoClient(CONNECTION_STRING)
    return client["test"]


async def main():
    if get_database() != None:
        print("Connection to database successful")
    else:
        print(Fore.RED + "ERROR: Failed to connect to database" + Fore.WHITE)
    async with serve(parse_request, "localhost", 8765):
        await asyncio.Future()


# REQUIRED REQUEST SYNTAX: "OPERATION, COLLECTION, QUERY"
async def parse_request(websocket):
    async for request in websocket:
        split_request = request.split(", ", 1)
        operation = split_request[0]
        message = split_request[1] if len(split_request) > 1 else ''
        print(request)
        if operation == "CREATE":
            create_document(message)
        elif operation == "READ":
            read_document(message)
        elif operation == "UPDATE":
            update_document(message)
        elif operation == "DELETE":
            delete_document(message)
        else:
            print(Fore.RED + "ERROR: Invalid Operation '" + operation + "'")
            today = date.today()
            cur_path = os.path.dirname(__file__)
            path_string = ".\\logs\\" + today.__str__() + ".txt"
            path_to_logfile = os.path.relpath(path_string, cur_path)
            with open(path_to_logfile, 'w') as logpath:
                logpath.write(datetime.now().__str__() + ": " + request)
            print("Incident has been logged." + Fore.WHITE)


#
# REQUIRED HELPER FUNCTION REQUEST SYNTAX: "COLLECTION, QUERY"
#

#
# REQUIRED QUERY SYNTAX: "{key_1:val_1,key_2:val_2...key_n-1:val_n-1,key_n:val_n}"
#

def parse_dictionary_from_query(query):
    dict = {}
    split_query = query.split(",")
    for key_value in split_query:
        split_key_value = key_value.split(":")
        key = split_key_value[0]
        value = split_key_value[1]
        dict[key] = value
    return dict


def create_document(request):
    split_request = request.split(", ", 1)
    collection = split_request[0]
    query = split_request[1] if len(split_request) > 1 else ''
    query_dict = parse_dictionary_from_query(query)
    db = get_database()
    db[collection].insert_one(query_dict)


def read_document(request):
    split_request = request.split(", ", 1)
    collection = split_request[0]
    query = split_request[1] if len(split_request) > 1 else ''
    query_dict = parse_dictionary_from_query(query)
    db = get_database()
    db[collection].find_one(query_dict)


def update_document(request):
    pass


def delete_document(request):
    split_request = request.split(", ", 1)
    collection = split_request[0]
    query = split_request[1] if len(split_request) > 1 else ''
    query_dict = parse_dictionary_from_query(query)
    db = get_database()
    db[collection].delete_one(query_dict)


asyncio.run(main())
