import asyncio
from .base_elemets import Span,Element
from microdot.websocket import with_websocket, WebSocket, WebSocketError
from microdot.microdot import Request
from .ringbuf_queue import RingbufQueue as Queue
import json

send_queue = {}
def dispatch_to_ws(obj):   
    data = "".join(obj) 
    item_to_pop = None
    print(data)
    for r,q in send_queue.items():
        try:
            q.put_nowait(data)
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
        if not hasattr(obj, '_reactive_values'):
            obj._reactive_values = {}
        if self not in obj._reactive_values:
            obj._reactive_values[self] = self.initial_value
        return obj._reactive_values[self]

    def __set__(self, obj, value):
        if not hasattr(obj, '_reactive_values'):
            obj._reactive_values = {}
        obj._reactive_values[self] = value

        if obj.dispatch_fn:
            type(obj).dispatch_fn(obj())

    

class ReactiveComponent:
    dispatch_fn = dispatch_to_ws

    def __init__(self) -> None:
        self.id = "id1-" + str(id(self))

    def __call__(self, *args, **kwds):
            return Span(self.render(),id=self.id)

    def render(self):
        raise NotImplementedError("Render method must be implemented by child classes")


@with_websocket
async def ws_sender(request:Request, ws: WebSocket):
    my_q= Queue(5)
    send_queue[request] = my_q
    try:
        while True:
            data = await my_q.get()
            await ws.send(data)
    except Exception as e:
        print("connection close", e)
        await ws.close()

@with_websocket
async def ws_reciver(request:Request,ws:WebSocket):

    try:
      while True:
            data = json.loads(await ws.receive())
            print(data)
            headers = data.pop('HEADERS')
            if headers["HX-Trigger-Name"] in  Element.callbacks_map:
                res = Element.callbacks_map[headers["HX-Trigger-Name"]](data)
            else:
                print("Callback not found")

            if res:
                dispatch_to_ws(res)
    except WebSocketError:
        print("connection close reciver")
        await ws.close()

        