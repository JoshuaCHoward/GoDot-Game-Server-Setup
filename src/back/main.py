import json
import uuid
import redis
import pika
import multiprocessing
import asyncio
from .pika_setup import PikaConnection
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from typing import Dict

socket_dict={}

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:3000",
    "127.0.0.1",
    "http://127.0.0.1",

]
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    socket_dict[websocket.client.host]=websocket
    id=str(uuid.uuid4())
    socket_dict['id']=websocket
    try:
        while True:
            try:
                byte_data = await websocket.receive_bytes()
                json_data=json.loads(byte_data.decode('UTF-8'))
                json_data['id']=id
                data=json.dumps(json_data)
            except:
                return
            await websocket.send_bytes(data.encode())
            PikaConnection.channel.basic_publish(exchange='', routing_key='hello', body=data)
    except WebSocketDisconnect:
        return


async def redis_start():
    bob_r = redis.Redis(host='localhost', port=6379, db=0)
    bob_p = bob_r.pubsub()
    bob_p.subscribe('classical_music')
    while True:
        message=bob_p.get_message()
        if (message!=None):
            if (message.get('id')==None):
                continue
            id=message["id"]
            socket:WebSocket=socket_dict[id]
            socket.send_text("NO BOY")
            print(message, "REDIS WORKED POGGERS")
        await asyncio.sleep(0.000001)

# def moving_events():
#     # connect with redis server as Bob
#     bob_r = redis.Redis(host='localhost', port=6379, db=0)
#     bob_p = bob_r.pubsub()
#     # subscribe to classical music
#     bob_p.subscribe('moving_creature')
#     redis_sub=bob_r.pipeline()
#     redis_sub.hmset("constant","test",(1,1))
#     redis_sub.hmget("constant","test")
#     a,b=redis_sub.execute()
#     while True:
#         message=bob_p.get_message()
#         if (message!=None):
#             if (message.get('id')==None):
#                 continue
#             id=message["id"]
#             socket:WebSocket=socket_dict[id]
#             socket.send_text("NO BOY")
#             print(message, "REDIS WORKED POGGERS")
#         await asyncio.sleep(0.000001)

bob_r = redis.Redis(host='localhost', port=6379, db=0)
bob_p = bob_r.pubsub()
@app.on_event("startup")
async def rabbitmq_setup():
    PikaConnection.startup()
    socket_dict['loop']=asyncio.get_event_loop()
    workers=1
    pool = multiprocessing.Pool(processes=workers)
    for i in range(0, workers):
        pool.apply_async(consume)
    # for i in range(0, workers):
    #     pool.apply_async(moving_events)
    channel = PikaConnection.channel
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    asyncio.create_task(redis_start())

    print(" [x] Sent 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa Worlsasads!'")


def consume_starter():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())


def consume():
    def callback(ch, method, properties, body):
        bob_r.publish("classical_music",body)
        print(" [x] Received %r" % body)
    PikaConnection.channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)
    PikaConnection.channel.start_consuming()


#