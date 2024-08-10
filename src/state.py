import asyncio
from base_elemets import Span
from lib.microdot.websocket import with_websocket, WebSocket
from lib.microdot.microdot import Request
from lib.ringbuf_queue import RingbufQueue as Queue


class State(object):
    def __init__(self) -> None:
        self.event = asyncio.Event()

    def __setattr__(self,name,value):
        super().__setattr__(name,value)
        self.event.set()

def reactive(f):
    def decorted(obj:State , *args,**kwargs):

        async def waiter():
            while True:
                await obj.event.wait()
                res = f(obj,*args,**kwargs).replace( ">" ," id='id-"+str(id(obj)) + "' >" , 1)
                dispatch_to_ws(res)
                obj.event.clear()

        asyncio.create_task(waiter())
        
        return f(obj,*args,**kwargs).replace( ">" ," id='id-"+str(id(obj)) + "' >" , 1)
    
    return decorted

ws_queues:dict[Request:asyncio.Queue] = {}
def dispatch_to_ws(obj):
    for r,q in ws_queues.items():
        try:
            q.put_nowait(obj)
        except IndexError:
            print("Poping", r)
            ws_queues.pop(r)


@with_websocket
async def ws_sender(request:Request, ws: WebSocket):
    my_queue = Queue(20)
    ws_queues[request] = my_queue
    try: 
        while True:
            f = await my_queue.get()
            await ws.send(f)
    except Exception:
        ws_queues.popitem(request)