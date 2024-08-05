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


async def main():
    app.mongodb_client = MongoClient("mongodb+srv://mirohaapalainen:05xiHzhyngidFSW7@chattercluster.ljuhfn2.mongodb.net/?retryWrites=true&w=majority&appName=ChatterCluster")
    app.database = app.mongodb_client["test"]
    print("Connection to database successful")
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
def create_document(request):
    pass


def read_document(request):
    pass


def update_document(request):
    pass


def delete_document(request):
    pass


asyncio.run(main())
