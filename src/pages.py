from base_elemets import Html,Head,Script,Link,Title,Body,Main


def template(content):
    return Html(
        Head(
            Script(src="gz/htmx.min.js.gz"),
            Link(rel="stylesheet", href="mvp.css"),
            Title("Thiss iss amazing")
        ),
        Body(
            Main(
                content

            )
        ),
        color_mode="user"
    )
