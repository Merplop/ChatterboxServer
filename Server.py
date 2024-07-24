from enum import Enum
import threading
import pymongo
from fastapi import FastAPI
from pymongo import MongoClient
import asyncio
from websockets.server import serve
from Request import Request

queue = []
app = FastAPI()

def command_loop():
    while(True):
        command = input(">")

async def echo(websocket):
    async for message in websocket:
        #await websocket.send(message)
        print(message)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()


def handle_request(request):
    if request.type == Request.Type.CREATE:
        create_document(request)
    elif request.type == Request.Type.READ:
        read_document(request)
    elif request.type == Request.Type.UPDATE:
        update_document(request)
    elif request.type == Request.Type.DELETE:
        delete_document(request)

def create_document(request):
    pass

def read_document(request):
    pass

def update_document(request):
    pass

def delete_document(request):
    pass

def loop_through_queue():
    while True:
        if not len(queue) == 0:
            request_to_process = queue.pop(0)
            handle_request(request_to_process)

asyncio.run(main())
