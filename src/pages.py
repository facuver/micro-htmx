from html_builder import Html_doc, Script, Link,Tag
try:
    from contextlib import contextmanager
    
except:
    from ucontextlib import contextmanager
    pass


@contextmanager
def template():
    with Html_doc() as (doc ,head,body) :
        with head:
            Tag("script", src="/htmx.min.js")
            Tag("link", rel="stylesheet", href="./simple.min.css")
            Tag("title", "This is Great!!")
        with body:
            header()
            yield doc


def header():
    with Tag("header"):
        Tag("span","Terest")
        Tag("span","Terest")
