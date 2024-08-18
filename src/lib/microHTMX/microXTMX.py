from microdot.microdot import Microdot, Response, send_file, URLPattern,redirect
from .base_elemets import Element, Html, Head, Script, Link, Body,Meta
from .state import ws_sender,ws_reciver


def add_head(*content):
    return (
        Html(
            Head(
                Meta(charset="UTF-8"),
                Script(src="public/gz/gz.htmx.min.js"),
                Script(src="public/gz/gz.ws.js"), 
                Link(rel="stylesheet", href="public\gz\gz.pico.zinc.min.css"),
                
            ),
            Body(*content, klass="container", ),       
        )
    )


class MicroHTMX(Microdot):

    def __init__(self):
        super().__init__()
        self.url_map.append(("GET", URLPattern("/ws_updates"), ws_sender))
        self.url_map.append(("GET", URLPattern("/ws_callbacks"), ws_reciver))
        Response.default_content_type = "text/html"

    def page(self, path):
        def decorator(f):
            @self.get(path)
            async def decorated(*args, **kwargs):
                resp = await f(*args, **kwargs)
                return add_head(resp)
            return decorated
        return decorator


app = MicroHTMX()


@app.route("public/gz/<file>")
async def _(request, file):
    return send_file(f"./public/gz/{file}", compressed=True)


@app.get("public/<file>")
async def _(request, file):
    return send_file(f"./public/{file}")
