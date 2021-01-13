# импортируем классы HTML, TopLevelTag, Tag из пакета utils модуля html
from utils.html import HTML, TopLevelTag, Tag

if __name__ == "__main__":
    # тестовый код для генерации HTML-тэгов из Python-документа
    with HTML(output="test.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head
        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="image/cat.png", width="200px", height="200px") as img:
                    div += img
                body += div
            doc += body