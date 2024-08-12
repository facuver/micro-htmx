import asyncio
from base_elemets import Span,Element
from microdot.websocket import with_websocket, WebSocket, WebSocketError
from microdot.microdot import Request
# from lib_src.ringbuf_queue import RingbufQueue as Queue
from lib_src.ringbuf_queue import RingbufQueue as Queue
import json

send_queue = {}
def dispatch_to_ws(obj):   
    item_to_pop  =None
    for r,q in send_queue.items():
        try:
            q.put_nowait(obj)
        except asyncio.QueueFull or IndexError or ConnectionAbortedError:
            item_to_pop = r
            print("queue full")

    if item_to_pop:
        send_queue.pop(item_to_pop)

class Reactive(object):
    callback = dispatch_to_ws
    def __init__(self) -> None:
        self.id = "id1-" + str(id(self))

    def render(self):
        raise NotImplementedError

    def __call__(self, *args, **kwds):
        return Span(self.render(),id=self.id) #.replace(">",f" id={self.id}>",1)
    
    def __setattr__(self,name,value):
        super().__setattr__(name,value)
        try:
            if self.callback:
                Reactive.callback(self())
        #object still not initialized
        except AttributeError:
            pass



@with_websocket
async def ws_sender(request:Request, ws: WebSocket):
    print("new ws")
    my_q= Queue(5)
    send_queue[request] = my_q
    try:
        while True:
            data = await my_q.get()
            await ws.send(data)
            
    except Exception as e:
        print("connection close", e)

@with_websocket
async def ws_reciver(request:Request,ws:WebSocket):
    try:
      while True:
            data = json.loads(await ws.receive())
            headers = data.pop('HEADERS')
            if headers["HX-Trigger-Name"] in  Element.callbacks_map:
                res = Element.callbacks_map[headers["HX-Trigger-Name"]](data)
                if res:
                    dispatch_to_ws(res)


            else:
                print("Callback not found")
    except WebSocketError:
        print("connection close reciver")