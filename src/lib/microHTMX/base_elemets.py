from typing import TypedDict, Literal
from typing_extensions import Unpack  # type: ignore


def chunk(gen, size=1024):
    buffer = bytearray(size)
    index = 0
    for item in gen:
        item_bytes = item.encode("utf-8")
        item_length = len(item_bytes)

        if index + item_length > size:
            # Yield current buffer content
            yield buffer[:index].decode("utf-8")

            # # Reset buffer and index
            # buffer = bytearray(size)
            index = 0

        # Copy new item into buffer
        buffer[index : index + item_length] = item_bytes
        index += item_length

        # If buffer is full, yield it
        if index == size:
            yield buffer.decode("utf-8")
            buffer = bytearray(size)
            index = 0

    # Yield any remaining content
    if index > 0:
        yield buffer[:index].decode("utf-8")


class KWARGS(TypedDict):
    hx_get: str
    hx_post: str
    hx_swap: Literal["innerHTML", "outerHTML", "textContent"]
    hx_target: str
    hx_trigger: str
    hx_on_click: str
    hx_push_url: str
    id: str
    value: str
    klass: str


class Element:
    callbacks_map = {}
    self_closing_tags = {"img", "input", "br", "hr", "meta", "link"}
    indent_level = 0
    indent_string = " "

    def __init__(self, name) -> None:
        self.name = name

    def __call__(self, *childs, callback=None, args=[], **kwargs: Unpack[KWARGS]):
        yield from self._render(childs, callback, args, kwargs)

    def _render(self, childs, callback, args, kwargs):
        if callback:
            el_id = kwargs.get("id", hex(hash(callback)))
            Element.callbacks_map[el_id] = callback
            kwargs["hx_post"] = f"/callbacks/{el_id}"

        # Generate opening tag
        yield f"\n{Element.indent_string *Element.indent_level}<{self.name}"

        # Generate attributes
        for key, value in kwargs.items():
            if value is False:
                value = "false"
            elif value is True:
                value = "true"

            if key == "klass":
                yield f" class='{value}'"
            else:
                yield f" {key.replace('_', '-')}='{value}'"

        for arg in args:
            yield f" {arg}"

        if self.name in self.self_closing_tags:
            yield "/>"
            return

        yield ">"

        if not childs:
            yield f"</{self.name}>"
            return

        Element.indent_level += 1
        # Generate child content
        for child in childs:
            if not isinstance(child, str):
                yield from child
            else:
                yield "\n" + Element.indent_string * Element.indent_level + str(child)

        # Generate closing tag
        Element.indent_level -= 1
        yield f"\n{Element.indent_string *Element.indent_level}</{self.name}>"


class Html(Element):
    def __init__(self):
        super().__init__("html")

    def __call__(self, *childs, args=[], **kwargs):
        yield "<!DOCTYPE html>"
        yield from super()._render(childs, None, args, kwargs)


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
