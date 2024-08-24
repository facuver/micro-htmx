import asyncio
import json

from microdot.websocket import with_websocket, WebSocket, WebSocketError
from microdot.sse import with_sse, SSE
from microdot.microdot import Request, Response

from .ringbuf_queue import RingbufQueue as Queue
from .base_elemets import Span, Element,H1,chunk

send_queue = {}


def dispatch_to_ws(obj):
    
    item_to_pop = None
    for r, q in send_queue.items():
        try:
            q.put_nowait(obj)
        except IndexError:
            item_to_pop = r
            print("queue full")

    if item_to_pop:
        send_queue.pop(item_to_pop)


class ReactiveProperty:
    def __init__(self, initial_value=None):
        self.initial_value = initial_value

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if not hasattr(obj, "_reactive_values"):
            obj._reactive_values = {}
        if self not in obj._reactive_values:
            obj._reactive_values[self] = self.initial_value
        return obj._reactive_values[self]

    def __set__(self, obj, value):
        if not hasattr(obj, "_reactive_values"):
            obj._reactive_values = {}
        obj._reactive_values[self] = value

        if obj.dispatch_fn:
            type(obj).dispatch_fn(obj)
import gc

class ReactiveComponent:
    dispatch_fn = dispatch_to_ws

    def __init__(self) -> None:
        self._id = "id1-" + str(id(self))

    def __call__(self, *args, **kwds):
        return Span(self.render(), sse_swap=self._id)

    def render(self):
        raise NotImplementedError("Render method must be implemented by child classes")

async def monkey_pached_send(self:SSE,element,event):
    msg = b'event: ' + event.encode() + b'\n'
    msg += b'data: '

    self.queue.append(msg)
    self.event.set()

    for c in chunk(element,1024):
        while not self.queue:
            await asyncio.sleep(0.1)

        print(gc.mem_free())
        self.queue.append(c.replace("\n",""))
        self.event.set()
    
    self.queue.append("\n\n")
    self.event.set()
    

@with_sse
async def sse_sender(request: Request, sse: SSE):
    my_q = Queue(5)
    send_queue[request] = my_q

    try:
        while True:
            data = await my_q.get()
            await monkey_pached_send(sse,data.render(), event=data._id)
    except IndexError as e:
        print("connection close", e)

async def callbacks_request(requets:Request,name):
    if name in Element.callbacks_map:
        bo = {}
        if requets.body:
            bo = {key:value for (key,value) in [s.split("=") for s in requets.body.decode("utf-8").split("&")] }
        res = Element.callbacks_map[name](bo)
        if res:
                return res
    else:
        print("Callback not found")

# @with_websocket
# async def ws_sender(request:Request, ws: WebSocket):
#     my_q= Queue(5)
#     send_queue[request] = my_q

#     @request.after_request
#     def _(request, response):
#         print("closing Request")
#         send_queue.pop(request)
#         response.already_handled = True
#         return response

#     try:
#         while True:
#             data = await my_q.get()
#             await ws.send(data)
#     except Exception as e:
#         print("connection close", e)


# @with_websocket
# async def ws_callbacks(request: Request, ws: WebSocket):

#     try:
#         while True:
#             data = json.loads(await ws.receive())
#             print(data)
#             headers = data.pop("HEADERS")
#             if headers["HX-Trigger-Name"] in Element.callbacks_map:
#                 res = Element.callbacks_map[headers["HX-Trigger-Name"]](data)
#                 if res:
#                     dispatch_to_ws(res)
#             else:
#                 print("Callback not found")

#     except WebSocketError:
#         print("connection close reciver")


