import asyncio
from base_elemets import Span,Element
from microdot.websocket import with_websocket, WebSocket
from microdot.microdot import Request
from ringbuf_queue import RingbufQueue as Queue
import json

class State(object):
    def __init__(self) -> None:
        # self.event = asyncio.Event()
        self.callbacks = []

    def __setattr__(self,name,value):
        super().__setattr__(name,value)
        print(name,self.callbacks)
        for c in self.callbacks:
            c()
        # self.event.set()



def reactive(f):
    def decorted(obj:State , *args,**kwargs):
        def add_id():
            return f(obj,*args,**kwargs).replace( ">" ," id='id-"+str(id(obj)) + "' >" , 1)
        obj.callbacks.append(lambda:dispatch_to_ws(add_id()))
        return add_id()

    return decorted


send_queue = Queue(5)
def dispatch_to_ws(obj):    
    try:
        send_queue.put_nowait(obj)
    except IndexError:
        print("queue full")

@with_websocket
async def ws_sender(request:Request, ws: WebSocket):
    while True:
        f = await send_queue.get()
        await ws.send(f)


@with_websocket
async def ws_reciver(request:Request,ws:WebSocket):
    while True:
        data = json.loads(await ws.receive())
        print( data)
        headers = data.pop('HEADERS')
        if headers["HX-Target"] in  Element.callbacks_map:
            
            Element.callbacks_map[headers["HX-Target"]](data)
