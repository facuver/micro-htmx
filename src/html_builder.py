
from typing import TypedDict
from typing_extensions import Unpack






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

    def __init__(self, tag: str, *children: List['Tag'], **kwargs: Unpack[KWARGS]) -> None:
        self.tag = tag

        conflicting_keys = [("klass", "class")] if "klass" in kwargs else []
        conflicting_keys.extend([(key, key.replace("_", "-")) for key in kwargs if "_" in key])
        self.kwargs = replace_keys(conflicting_keys, kwargs)
        
        self.children = list(children) 

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
        slot = ""
        if self.children:
            if isinstance(self.children[0], Tag):
                header += "\n"
                footer = f"{indent}{footer}"

            for child in self.children:
                if isinstance(child, Tag):
                    slot += child.__str__(level + 1)
                else:
                    slot += child


        return header + slot + footer
    

    def __repr__(self) -> str:
        return f"<{self.tag.capitalize()}{self.kwargs if self.kwargs else ""} [{  ','.join([c.tag for c in self.children])  }]>"

    def append(self, tag: 'Tag'):
        self.children.append(tag)



class Input(Tag):
    def __init__(self,**kwargs: Unpack[KWARGS]) -> None:
        super().__init__("input",  **kwargs)

class Button(Tag):
    def __init__(self, *children,**kwargs: Unpack[KWARGS]) -> None:
        super().__init__("button", *children, **kwargs)
        
class Div(Tag):
    def __init__(self, text="", *args, **kwargs) -> None:
        super().__init__("div", text, *args, **kwargs)

class H1(Tag):
    def __init__(self,  *children,**kwargs: Unpack[KWARGS]) -> None:
        super().__init__("h1", *children, **kwargs)



class Html_doc(Tag):
    def __init__(self,*children, **kwargs: Unpack[KWARGS]) -> None:
        super().__init__("html", *children, **kwargs)

    def __enter__(self):
        html = super().__enter__()
        header = Tag("head")
        body = Tag("body")
        return html,header,body
    

class Card(Tag):
    def __init__(self,*children, **kwargs: Unpack[KWARGS]) -> None:
        super().__init__("div", *children, **kwargs)

    def __enter__(self):
        card = super().__enter__()
        header = Tag("div")
        body = Tag("div")
        return card,header,body
    
    

Script = lambda *args,**kwargs: Tag("sript",*args,**kwargs)
Link = lambda *args,**kwargs: Tag("link",*args,**kwargs)

