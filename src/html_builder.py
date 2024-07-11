from ucontextlib import contextmanager

from typing import TypedDict 
try:
    from typing_extensions import Unpack
except:
    pass




class KWARGS(TypedDict):
    hx_get: str
    hx_post: str
    hx_swap: str
    hx_target: str
    hx_trigger: str
    hx_push_url: str
    id: str
    value:str
    klass:str




@contextmanager
def template():
    with Tag("html", klass="") as html:
        with Tag("head"):
            Tag("script", src="/htmx.min.js")
            Tag("link", rel="stylesheet", href="./simple.min.css")
            Tag("title", "This is Great!!")
        with Tag("body"):
            header()
            yield html


def header():
    with Tag("header"):
        Tag("span","Terest")
        Tag("span","Terest")


from typing import List, Dict, Any, Tuple
from collections import deque

# Ensure this function exists
def replace_keys(conflinting_keys: List[Tuple[str, str]], kwargs: Dict[str, Any]) -> Dict[str, Any]:
    for old_key, new_key in conflinting_keys:
        if old_key in kwargs:
            kwargs[new_key] = kwargs.pop(old_key)
    return kwargs

class Tag:
    stack = []

    def __init__(self, tag: str, children: List['Tag'] = None, **kwargs: Unpack[KWARGS]) -> None:
        self.tag = tag

        conflicting_keys = [("klass", "class")] if "klass" in kwargs else []
        conflicting_keys.extend([(key, key.replace("_", "-")) for key in kwargs if "_" in key])
        self.kwargs = replace_keys(conflicting_keys, kwargs)
        
        self.children = children if children is not None else []

        if Tag.stack:
            Tag.stack[-1].append(self)
    
    def __enter__(self):
        Tag.stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        Tag.stack.pop()
        return True


    def __str__(self, level=0):
        indent = '  ' * level
        kwargs_str = " ".join([f"{key}='{value}'" for key, value in self.kwargs.items()])
        header = f"{indent}<{self.tag} {kwargs_str}>"
        footer = f"</{self.tag}>\n"
        if self.children:
            if isinstance(self.children[0], Tag):
                header += "\n"
                footer = f"{indent}{footer}"



        slot = ""
        for child in self.children:
            if isinstance(child, Tag):
                slot += child.__str__(level + 1)
            else:
                slot += f"{child}"
        return header + slot + footer
    
    def append(self, tag: 'Tag'):
        self.children.append(tag)

class Input(Tag):
    def __init__(self,**kwargs: Unpack[KWARGS]) -> None:
        super().__init__("input",  **kwargs)

class Button(Tag):
    def __init__(self, children: List[Tag] = None,**kwargs: Unpack[KWARGS]) -> None:
        super().__init__("button", children, **kwargs)
        
class Div(Tag):
    def __init__(self, text="", *args, **kwargs) -> None:
        super().__init__("div", text, *args, **kwargs)

class H1(Tag):
    def __init__(self,  children: List[Tag] = None,**kwargs: Unpack[KWARGS]) -> None:
        super().__init__("h1", children, **kwargs)