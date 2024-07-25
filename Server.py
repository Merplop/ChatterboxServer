from enum import Enum
import threading
import pymongo
from fastapi import FastAPI
from pymongo import MongoClient
import asyncio
from websockets.server import serve
from Request import Request
from colorama import Fore

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
        split_request = request.split(',', 1)
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
            print(Fore.RED + 'ERROR:')
            print("Invalid Operation")


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
