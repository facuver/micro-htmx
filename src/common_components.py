from lib.microHTMX.base_elemets import Html,Head,Script,Link,Title,Body,Main,Header,Footer,Nav,Ul,Li,A,Strong,Style,Div,Span

def navBar(current_path):
    print(current_path)
    def A_or_Stong(path:str):
        if path == current_path:
            return Strong(path[1:].upper() )
        return A(path[1:].upper() , href=path)
    
    paths = [Li(A_or_Stong(p)) for p in ["/home","/about", "/gpio"]]

    return  Nav(
            
        Ul(
            A(Strong("RP2040"),href="/home")
        ),
        Ul(
            *paths
        )
    )

def page_template(*content , path = "/"):
    yield from Header(navBar(path),klass="container")
    yield from Main(*content,klass="h-screen bg-purple-400 flex items-center justify-center", hx_ext="ws", ws_connect="/ws_callbacks")




