






class Page:
    """需要翻译的一本书的一页内容"""


    def __init__(self):
        self.content = []


    def add_content(self, content):
        self.content.append(content)