from html_builder import *
try:
    from contextlib import contextmanager
    
except:
    from ucontextlib import contextmanager
    pass


def tabs(selected=1):
    with Ul(klass="nav",hx_swap="outerHTML", id="tabs",hx_target="#tabs" ) as d:
        for i in range(1,4):
            with Li():
                A(f"Tab {i}" ,href="#",hx_get=f"/tab/{i}",klass= 'nav-item active' if selected == i else 'nav-item')  
    return d



def tabs1(selected=1):
    with Ul(klass="nav"):
        with Li(klass="nav-item"):
            A("Elements",href="#")            

@contextmanager
def template():
    with Html_doc() as (doc ,head,body) :
        with head:
            Tag("link", rel="stylesheet", href="https://unpkg.com/mvp.css")
            Tag("script", src="/htmx.min.js")
            Tag("script", src="/ws.js")
            Tag("title", "This is Great!!")


        with body:
            body.kwargs["class"] = "container"
            tabs()
            yield doc


def header():
    with Tag("header"):
        Tag("span","Terest")
        Tag("span","Terest")
