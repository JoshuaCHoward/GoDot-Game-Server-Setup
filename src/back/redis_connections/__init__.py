# import redis
#
# class RedisConnection:
#     redis_connection:BlockingConnection = None
#     channel: BlockingChannel = None
#
#     @classmethod
#     def startup(cls):
#         connection = redis.Redis(host='localhost', port=6379, db=0)
#         channel = connection.channel()
#         channel.queue_declare(queue='hello')
#         PikaConnection.pika_connection = connection
#         PikaConnection.channel = channel
#
#     @classmethod
#     async def redis_start():
#         bob_r = redis.Redis(host='localhost', port=6379, db=0)
#         bob_p = bob_r.pubsub()
#         bob_p.subscribe('classical_music')
#         while True:
#             message=bob_p.get_message()
#             if (message!=None):
#                 if (message.get('id')==None):
#                     continue
#                 id=message["id"]
#                 socket:WebSocket=socket_dict[id]
#                 socket.send_text("NO BOY")
#                 print(message, "REDIS WORKED POGGERS")
#             await asyncio.sleep(0.000001)
