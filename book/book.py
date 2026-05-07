




class Book:
    """需要翻译的一本书"""
    def __init__(self, file_path):
        self.file_path = file_path
        self.pages = []

    def add_page(self, page):
        self.pages.append(page)


