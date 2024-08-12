from microdot.microdot import Microdot, Response, send_file, URLPattern,redirect
from base_elemets import Element, Html, Head, Script, Link, Body,Meta
from state import ws_sender,ws_reciver


def add_head(*content):
    return (
        Html(
            Head(
                Meta(charset="UTF-8"),
                Script(src="public/gz/gz.htmx.min.js"),
                Script(src="public/gz/gz.ws.js"),
                Link(rel="stylesheet", href="public/gz/gz.pico.zinc.min.css"),
                
            ),
            Body(*content, klass="container", ),       
        ),
    )


class MicroHTMX(Microdot):
    def route(self, url_pattern, methods=None):
        def decorated(f):
            async def r(*args, **kwargs):
                resp = await f(*args, **kwargs)
                if isinstance(resp, Response):
                    return resp
                if isinstance(resp, tuple):
                    resp = " ".join(resp)
                return Response(resp, headers={"Content-Type": "text/html"})

            self.url_map.append(
                ([m.upper() for m in (methods or ["GET"])], URLPattern(url_pattern), r)
            )
            return r

        return decorated

    def page(self, path):
        def decorator(f):
            @self.get(path)
            async def decorated(*args, **kwargs):
                resp = await f(*args, **kwargs)
                if isinstance(resp, tuple):
                    resp = " ".join(resp)
                return add_head(resp)

            return decorated

        return decorator


app = MicroHTMX()


app.url_map.append(("GET", URLPattern("/ws_updates"), ws_sender))
app.url_map.append(("GET", URLPattern("/ws_callbacks"), ws_reciver))


@app.post("callbacks/<id>")
async def _(request, id):
    try:
        body = {}
        if request.body:
            body = {
                key: value
                for key, value in [
                    p.split("=") for p in request.body.decode("utf-8").split("&")
                ]
            }

        resp = Element.callbacks_map[id](body)

        if isinstance(resp, str):
            return resp
    except KeyError:
        print("keyError")
        return """<meta http-equiv="refresh" content="0" >"""
    return


@app.route("public/gz/<file>")
async def _(request, file):
    return send_file(f"./public/gz/{file}", compressed=True)


@app.get("public/<file>")
async def _(request, file):
    return send_file(f"./public/{file}")
