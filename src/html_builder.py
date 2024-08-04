from typing import TypedDict ,Literal
from typing_extensions import Unpack
from microdot.microdot import Microdot, Response


callbacks_app = Microdot()

@callbacks_app.post("/<id>")
def _(request,id):
    val=""
    if b"=" in request.body:
        val = request.body.decode("utf-8").split("=")[1]
    
    resp = callbacks_map[id](val)
    if isinstance(resp,str):
        return resp
    return 


Response.default_content_type = "text/html"

callbacks_map ={}

class KWARGS(TypedDict):
    hx_get: str
    hx_post: str
    hx_swap: Literal["innerHTML", "outerHTML", "textContent"]
    hx_target: str
    hx_trigger: str
    hx_on_click: str
    hx_push_url: str
    id: str
    value:str
    klass:str

class Element:
    self_closing_tags = {'img', 'input', 'br', 'hr', 'meta', 'link'}
    always_closing_tags = {'script', 'style'}

    def __init__(self, name) -> None:
        self.name = name
    
    def __call__(self, *childs, callback=None,args=[], **kwargs:Unpack[KWARGS]):
        if callback:
            id_int = id(callback)
            callbacks_map[str(id_int)] = callback
            kwargs["hx_post"]=f"/callbacks/{id_int}"

        # Convert kwargs keys from underscore to hyphen and handle 'klass'
        converted_kwargs = {}
        for key, value in kwargs.items():
            if key == 'klass':
                converted_kwargs['class'] = value
            else:
                converted_kwargs[key.replace('_', '-')] = value
        
        attrs = ' '.join(args + [f"{key}='{val}'" for key, val in converted_kwargs.items()])
        open_tag = f"<{self.name}{' ' + attrs if attrs else ''}>"
        
        if self.name in self.self_closing_tags:
            return open_tag
        
        if not childs:
            if self.name in self.always_closing_tags:
                return f"{open_tag}</{self.name}>"
            return open_tag
        
        content = '\n'.join(
            child for child in childs
        )
        
        return f"{open_tag}\n{content}\n</{self.name}>"
        

class Html(Element):
    def __init__(self):
        super().__init__('html')

    def __call__(self, *childs, args=[], **kwargs):
        doctype = "<!DOCTYPE html>"
        html_content = super().__call__(*childs, args=args, **kwargs)
        return f"{doctype}\n{html_content}"


