from microdot.microdot import Microdot, Response, send_file, URLPattern,redirect , MUTED_SOCKET_ERRORS
from .base_elemets import Element, Html, Head, Script, Link, Body,Meta,Span
from .state import ws_callbacks,sse_sender,callbacks_request
import asyncio

MUTED_SOCKET_ERRORS.extend([64,10053])

class MicroHTMX(Microdot):

    def __init__(self, reactive=False):
        super().__init__()
        if reactive:
            # self.url_map.append(("GET", URLPattern("/ws_updates"), ws_sender))
            self.url_map.append(("GET", URLPattern("/sse_updates"), sse_sender))

        # self.url_map.append(("GET", URLPattern("/ws_callbacks"), ws_callbacks))
        self.url_map.append(("POST", URLPattern("/callbacks/<name>"), callbacks_request))
        self.url_map.append(("GET", URLPattern("public/gz/<file>"), lambda _,file: send_file(f"./public/gz/{file}", compressed=True , max_age=3600) ))
        self.url_map.append(("GET", URLPattern("public/<file>"), lambda _,file: send_file(f"./public/{file}",max_age=3600) ))
        
        Response.default_content_type = "text/html"
        self.reactive= reactive


    def run(self, host='0.0.0.0', port=5000, debug=False, ssl=None):

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self.start_server(host=host, port=port, debug=debug,
                                      ssl=ssl))
        except:
            asyncio.run(self.start_server(host=host, port=port, debug=debug,
                                      ssl=ssl))
    def page(self, path):
        def decorator(f):
            @self.get(path)
            async def decorated(*args, **kwargs):
                resp = await f(*args, **kwargs)
                return self.add_head(resp)
            return decorated
        return decorator
    
    
    def add_head(self,*content ):
        return (
            Html(
                Head(
                    Meta(charset="UTF-8"),
                    Script(src="public/gz/gz.htmx.min.js"),
                    Script(src="public/gz/gz.sse.js") if self.reactive else ""  , 
                    Link(rel="stylesheet", href="public/gz/gz.pico.zinc.min.css"),

                    
                ),
                Body(*content, klass="container", **({"hx_ext":"sse", "sse-connect":"/sse_updates"} if self.reactive else {})),       
            )
        )




