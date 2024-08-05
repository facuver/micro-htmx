
from pages import template
from microdot.microdot import Microdot, Response, send_file
from base_elemets import Element

callbacks_app = Microdot()
app = Microdot()

def page(path):
    def decorator(f):
        @app.get(path)
        async def decorated(*args,**kwargs):
            resp = await f(*args,**kwargs)
            if isinstance(resp,str):
                print("all good")
            if isinstance(resp,tuple):
                resp = " ".join(resp)
            return Response(template(resp),headers={"Content-Type":"text/html"})
        return decorated
    return decorator
        
@app.post("callbacks/<id>")
async def _(request,id):
    body = {}
    if request.body:
        body = {key:value for key,value in [p.split("=") for p in request.body.decode("utf-8").split("&")] }
    
    resp = Element.callbacks_map[id](body)
    if isinstance(resp,str):
        return resp
    return 


@app.get("public/gz/<file>")
async def _(request, file):
    return send_file(f"./public/gz/{file}",compressed=True)

@app.get("public/<file>")
async def _(request, file):
    return send_file(f"./public/{file}")
