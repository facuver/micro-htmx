
import asyncio
from lib.microdot.microdot import Microdot, Response, send_file,URLPattern 
from lib.microdot.sse import with_sse, SSE
from base_elemets import Element,Html,Head,Script,Link,Body

def add_head(*content):
    return Html(
        Head(
            Script(src="public/gz/gz.htmx.min.js"),
            Link(rel="stylesheet", href="public/gz/gz.pico.zinc.min.css"),
            '<script src="https://unpkg.com/htmx-ext-ws@2.0.0/ws.js"></script>'
        ),
        Body(

            *content,
            klass="container",
            color_mode="user"

            ),
        )
Response.default_content_type = "text/html"
class MicroHTMX(Microdot):
    # def route(self, url_pattern, methods=None):
    #     def decorated(f):
    #         async def r(*args,**kwargs):
    #             resp = await f(*args,**kwargs)
    #             if isinstance(resp, Response):
    #                 return resp
    #             # if isinstance(resp,tuple):
    #             #     resp = " ".join(resp)
    #             return Response(resp,headers={"Content-Type":"text/html"})
    #         self.url_map.append(
    #             ([m.upper() for m in (methods or ['GET'])],
    #              URLPattern(url_pattern), r))
    #         return r
    #     return decorated
    

    def page(self,path):
        def decorator(f):
            @self.get(path)
            async def decorated(*args,**kwargs):
                resp = await f(*args,**kwargs)
                if isinstance(resp,tuple):
                    resp = " ".join(resp)
                return add_head(resp)
            return decorated
        return decorator
    
    
app = MicroHTMX()




        
@app.post("callbacks/<id>")
async def _(request,id):
    body = {}
    print(request.body)
    if request.body:
        body = {key:value for key,value in [p.split("=") for p in request.body.decode("utf-8").split("&")] }
    
    resp = Element.callbacks_map[id](body)
    if isinstance(resp,str):
        return resp
    return 

@app.route('/events')
@with_sse
async def events(request, sse:SSE):
    # send an unnamed event with string data
    for i in range(20):
        await asyncio.sleep(.11)
        await sse.send(f'hello {i}', event='message')
    await sse.send("Net")
    await sse.send("Net",event="close")

@app.route("public/gz/<file>")
async def _(request, file):
    return send_file(f"./public/gz/{file}",compressed=True)

@app.get("public/<file>")
async def _(request, file):
    return send_file(f"./public/{file}")

