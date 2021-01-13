class HTML:
    def __init__(self, tag='html', output=None):
        self.tag = tag
        self.output = output
        self.children_tags = []
            
    def __enter__(self):
        return self
    
    def __iadd__(self, other):
        """ Добавление дочернего тэга в список children_tags 
        при выполнении операции +="""
        self.children_tags.append(str(other))
        return self
    
    def __exit__(self, type, value, traceback):
        """ Вывод тэга html и всех его дочерних тэгов в файл, если 
        задано имя файла, иначе - вывод на экран """
        if self.output is None:
            print("<%s>" % self.tag)
            print("\n".join([child for child in self.children_tags]))
            print("</%s>" % self.tag)
        else:
            with open(self.output, "w") as html:
                html.write("<%s>" % self.tag)
                html.write("\n".join([child for child in self.children_tags]))
                html.write("</%s>" % self.tag)

class TopLevelTag(HTML):
    def __str__(self):
        """ Возврат сгенерированного тэга класса TopLevelTag и всех его дочерних тэгов
        при вызове функции str() """
        return "   <{tag}>\n{children}   </{tag}>".format(tag=self.tag, children="".join(self.children_tags))
    
    def __exit__(self, type, value, traceback):
        return self

class Tag(TopLevelTag):
    def __init__(self, tag, is_single = False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.children_tags = []
        self.is_single = is_single
        
        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value
    
    def __str__(self):
        """ Возврат сгенерированного тэга класса Tag и всех его дочерних тэгов с атрибутами
        при вызове функции str() """
        attrs = " ".join('%s="%s"' % (attribute, value)
                        for attribute, value in self.attributes.items())
        if self.children_tags:
            opening = "      <{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children_tags:
                internal += "   "+str(child)
            ending = "      </%s>\n" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "      <{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)
            else:
                return "      <{tag} {attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text)

