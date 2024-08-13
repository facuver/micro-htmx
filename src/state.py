import asyncio
from base_elemets import Span,Element
from lib_src.microdot.websocket import with_websocket, WebSocket, WebSocketError
from lib_src.microdot.microdot import Request
from lib_src.ringbuf_queue import RingbufQueue as Queue
import json

class State(object):
    def __init__(self) -> None:
        self.callback = None
        self.id = "id1-" + str(id(self))

    # def init(self):
    #     self.callback = dispatch_to_ws

    def render(self):
        raise NotImplementedError

    def __call__(self, *args, **kwds):
        return Span(self.render(),id=self.id) #.replace(">",f" id={self.id}>",1)
    
    def __setattr__(self,name,value):
        super().__setattr__(name,value)
        if self.callback:
            self.callback(self())



# def reactive(f):
#     def decorted(obj:State , *args,**kwargs):
#         def add_id():
#             return f(obj,*args,**kwargs).replace( ">" ," id='id-"+str(id(obj)) + "' >" , 1)
#         obj.callbacks.append(lambda:dispatch_to_ws(add_id()))
#         return add_id()

#     return decorted


send_queue = {}
def dispatch_to_ws(obj):   
    data = "".join(obj) 
    print(data)
    for r,q in send_queue.items():
        try:
            q.put_nowait(data)
        except IndexError:
            print("queue full")

@with_websocket
async def ws_sender(request:Request, ws: WebSocket):
    my_q= Queue(5)
    send_queue[request] = my_q
    try:
        while True:
            data = await my_q.get()
            print(data[20:])
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

        