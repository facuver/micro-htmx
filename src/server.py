from microdot.microdot import Microdot , Response,send_file,Request
from microdot.websocket import with_websocket , WebSocket
import asyncio
from html_builder import *
from pages import template,tabs
import utime as time
import json, machine


def send_tag(tag:Tag):
    return Response(tag.render(),headers={'Content-Type': 'text/html'})

html = lambda x: x   #hack to get code linting on vscode

app = Microdot()
led = machine.Pin("LED",machine.Pin.OUT)

def time_tag():
    return Div(str(time.ticks_ms()) , id="notifications").render()

@app.get("/")
async def _(request):
    with template() as t:
        

        with Div(hx_ext="ws", ws_connect="/echo"):
            time_tag()
            Div(text="...",id="chat_room")
            with Form(id="form",ws_send="true"):
                Button("ClickMe",)
                Input(name="chat_message")
                
    return send_tag(t)


@app.route('/echo')
@with_websocket
async def echo(request, ws:WebSocket):

    while True:
        data =json.loads( await  ws.receive())
        #print(data)
        led.toggle()
        #await asyncio.sleep(0.10)
        await ws.send(time_tag())
    

@app.route("/tab/<id>")
async def _(request,id):
        return send_tag(tabs(int(id)))



@app.route('/<file>')

async def public(request,file):
    return send_file(f"./public/{file}")
    

def run():
    app.run(debug= True,port=80)
  

if __name__ =="__main__":
    run()