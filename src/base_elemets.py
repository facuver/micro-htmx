from typing import TypedDict ,Literal
from typing_extensions import Unpack # type: ignore
import gc

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

class Element_old:
    callbacks_map = {}
    self_closing_tags = {'img', 'input', 'br', 'hr', 'meta', 'link'}
    always_closing_tags = {'script', 'style','div'}

    def __init__(self, name) -> None:
        self.name = name
    
    def __call__(self, *childs, callback=None, args=[], **kwargs:Unpack[KWARGS]):
        if callback:
            if "id" in kwargs:
                el_id = kwargs["id"]
            else:
                el_id = hex(hash(callback))
            Element.callbacks_map[el_id] = callback
            kwargs["ws-send"]="true"
            kwargs["name"]=el_id
        # Convert kwargs keys from underscore to hyphen and handle 'klass'
        converted_kwargs = {}
        for key, value in kwargs.items():

            if value is False:
                value = "false"
            if value is True:
                value ="true"

            if key == 'klass':
                converted_kwargs['class'] = value
            else:
                converted_kwargs[key.replace('_', '-')] = value


        


        
        
        attrs = ' '.join(args + [f"{key}='{val}'" for key, val in converted_kwargs.items()])
        open_tag = f"<{self.name}{' ' + attrs if attrs else ''}>"
        
        if self.name in self.self_closing_tags:
            return open_tag
        
        content = '\n'.join(
            child for child in childs
        )
        
        return f"{open_tag}\n{content}</{self.name}>"
      
class Element:
    callbacks_map = {}
    self_closing_tags = {'img', 'input', 'br', 'hr', 'meta', 'link'}
    always_closing_tags = {'script', 'style', 'div'}

    def __init__(self, name):
        self.name = name
   

   
    def __call__(self, *childs, callback=None, args=[], **kwargs):
        return "".join(self._render(childs, callback, args, kwargs))
    
    def _render(self, childs, callback, args, kwargs):
        if callback:
            el_id = kwargs.get("id", hex(id(callback)))
            Element.callbacks_map[el_id] = callback
            kwargs["ws-send"] = "true"
            kwargs["name"] = el_id
        
        resp =  f"<{self.name}"
        
        for key, value in kwargs.items():
            if value is False:
                value = "false"
            elif value is True:
                value = "true"
            
            if key == 'klass':
                resp += f" class='{value}'"
            else:
                resp += f" {key.replace('_', '-')}='{value}'"
        
        for arg in args:
            resp += f" {arg}"
        
        if self.name in self.self_closing_tags:
            resp += "/>"
            yield resp
            return
        
        resp += ">\n"
        yield resp
            
        for child in childs:
            if isinstance(child, str):
                yield str(child)
            else:
                yield from child
        
        yield f"</{self.name}>"


class Html(Element):
    def __init__(self):
        super().__init__('html')
    
    def __call__(self, *childs, args=[], **kwargs):
        yield "<!DOCTYPE html>"
        yield from super()._render(childs, None, args, kwargs)
    

def chain(*iterators):
    for i in iterators:
        yield from i

def render_html(generator):
    return ''.join(generator)

# Basic HTML tags
Html = Html()
Head = Element("head")
Body = Element("body")
Title = Element("title")
Meta = Element("meta")
Link = Element("link")
Script = Element("script")
Style = Element("style")
Noscript = Element("noscript")

# Structure
Div = Element("div")
Span = Element("span")
Header = Element("header")
Nav = Element("nav")
Main = Element("main")
Article = Element("article")
Section = Element("section")
Aside = Element("aside")
Footer = Element("footer")

# Text content
H1 = Element("h1")
H2 = Element("h2")
H3 = Element("h3")
H4 = Element("h4")
H5 = Element("h5")
H6 = Element("h6")
P = Element("p")
Blockquote = Element("blockquote")
Pre = Element("pre")
Code = Element("code")

# Inline text semantics
A = Element("a")
Strong = Element("strong")
Em = Element("em")
Small = Element("small")
S = Element("s")
Cite = Element("cite")
Q = Element("q")
Dfn = Element("dfn")
Abbr = Element("abbr")
Time = Element("time")
Br = Element("br")

# Image and multimedia
Img = Element("img")
Audio = Element("audio")
Video = Element("video")
Source = Element("source")

# Lists
Ul = Element("ul")
Ol = Element("ol")
Li = Element("li")
Dl = Element("dl")
Dt = Element("dt")
Dd = Element("dd")

# Table content
Table = Element("table")
Caption = Element("caption")
Thead = Element("thead")
Tbody = Element("tbody")
Tfoot = Element("tfoot")
Tr = Element("tr")
Th = Element("th")
Td = Element("td")

# Forms
Form = Element("form")
Label = Element("label")
Input = Element("input")
Button = Element("button")
Select = Element("select")
Option = Element("option")
Textarea = Element("textarea")
Fieldset = Element("fieldset")
Legend = Element("legend")
