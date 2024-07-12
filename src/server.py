from microdot.microdot import Microdot , Response,send_file,Request
from microdot import sse
import asyncio
from html_builder import Tag,Button, H1,Input
from pages import template


def send_tag(tag):
    return Response(str(tag),headers={'Content-Type': 'text/html'})

app = Microdot()
api = Microdot()


def parse_htmx_body(body:bytearray):
    sting = body.decode("utf-8")
    return sting.split("=")
    print(sting)


@api.post("/clicked")
async def _(request:Request):
    name,val  = parse_htmx_body(request.body)

    return send_tag( Tag("button",val,hx_post="/api/clicked",hx_swap="outerHTML",id="but"))

@app.get("/")
async def _(request):
    with template() as t:
        H1("Title")
        Input(placeholder="Put something", hx_trigger="keyup changed delay:500ms" , hx_post="/api/clicked",name = "input",hx_target="#but",hx_swap="outerHTML")
        Button("click!",hx_post="/api/clicked",hx_swap="outerHTML",id="but")
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