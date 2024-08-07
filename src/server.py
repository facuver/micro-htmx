import asyncio
import gc
from lib.ringbuf_queue import RingbufQueue as Queue
from base_elemets import Div, Input, Button, Form, Aside, Nav, Li, Ul, H1, Span  # noqa: F403
from common_components import page_template
from microXTMX import app
from lib.microdot.websocket import with_websocket, WebSocket
from lib.microdot.microdot import Request



ws_queues:dict[Request:asyncio.Queue] = {}
class State:
    value = 10
    callbacks = []

    @classmethod
    def set_state(cls, value):
        cls.value = value
        print(value)
        for c in cls.callbacks:
            c(cls)

def reactive(f):
    State.callbacks.append(lambda x: (f(x)))
    return f


@reactive
def Test(v: State):
    return H1(str(v.value), id="id-"+str(id(State)))

@app.after_request
def _(r,res):
    gc.collect()

@app.page("/")
async def _(request):
    return page_template(
        Span(hx_ext="ws", ws_connect="/ws"),
        Test(State),
        Test(State),
        Button("ADD", callback=lambda x: State.set_state(State.value + 1)),
    )


@app.page("/next")
async def _(request):
    return page_template("Next")

def dispatch_to_ws(obj):

    for q in ws_queues.values():
        try:
            q.put_nowait(obj)
        except IndexError:
            print("Full queue")


@app.get("/ws")
@with_websocket
async def _(request:Request, ws: WebSocket):
    my_queue = Queue(20)
    
    ws_queues[request] = my_queue
    try: 
        while True:
            f = await my_queue.get()

            print(f)
            await ws.send(f)
            # await ws.close()
    except:
        ws_queues.popitem(request)


def run():
    app.run(debug=True)


if __name__ == "__main__":
    run()
