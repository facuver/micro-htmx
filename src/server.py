from microdot.microdot import Microdot , Response,send_file
from microdot import sse
import asyncio
from html_builder import Tag,template,Button, H1,Input


from machine import Pin


led = Pin("LED",Pin.OUT)

led.on()


def send_tag(tag):
    return Response(str(tag),headers={'Content-Type': 'text/html'})

app = Microdot()
api = Microdot()




@api.post("/clicked")
async def _(request):
    global led
    led.toggle()
    return send_tag( Tag("button",f"Tunr {"on" if led.value() == 0 else "off"}!!",hx_post="/api/clicked",hx_swap="outerHTML"))

@app.get("/")
async def _(request):
    with template() as t:
        H1("Title")
        Input(value="HELLP")
        Button("click!",hx_post="/api/clicked",hx_swap="outerHTML")
    return send_tag(t)




@app.route('/events')
@sse.with_sse
async def events(request, sse):
    for i in range(3):
        await asyncio.sleep(1)
        await sse.send(i, event = "message")  # unnamed event+
    
    await sse.send("close",event="close")  # named event



@app.route('/<file>')
async def public(request,file):
    return send_file(f"./public/{file}")


def run():
    app.mount(api,"/api")
    app.run(debug= True)
  

if __name__ =="__main__":
    run()