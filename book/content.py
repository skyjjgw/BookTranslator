import json
from enum import Enum, auto
import pandas as pd

class ContentType(Enum):
    """Types of content, such as text, images, and tables.
    """
    TEXT = auto()
    IMAGE = auto()
    TABLE = auto()
class Content:
    """Content of a book, including title, author, and chapters.
    """
    def __init__(self, content_type, original, translation=None):
        """初始化内容对象
        :param content_type: 内容类型，如文本、图片、表格等
        :param original: 原始内容，如原文文本、原始图片等
        :param translation: 翻译后的内容，如翻译文本、翻译图片等
        """
        self.original = original
        self.translation = translation
        self.content_type = content_type
        self.status = False #翻译状态，默认为False，表示未翻译；翻译完成后设置为True


    def set_translation(self,translation,status):
        """设置翻译内容和状态
        :param translation: 翻译后的内容
        :param status: 翻译状态，True表示翻译完成，False表示未翻译
        """
        if self.content_type == ContentType.TEXT and self.status == False:
            self.translation = translation
            self.status = status #翻译完成，设置状态为True

    def get_origianl_to_string(self):
        """获取原始内容的字符串表示
         :return: 原始内容的字符串表示
         """
        pass


class TableContent(Content):
    """Table of contents, including chapter titles and page numbers.
    """
    def __init__(self, content_type, original, translation=None):
        """初始化内容对象
        :param content_type: 内容类型，如文本、图片、表格等
        :param original: 原始内容，如原文文本、原始图片等
        :param translation: 翻译后的内容，如翻译文本、翻译图片等
        """
        self.original = pd.DataFrame(original)
        self.translation = translation
        self.content_type = content_type
        self.status = False #翻译状态，默认为False，表示未翻译；翻译完成后设置为True

    def set_translation(self, translation, status):
        """设置翻译内容和状态
        :param translation: 翻译后的内容
        :param status: 翻译状态，True表示翻译完成，False表示未翻译
        """
        if self.content_type == ContentType.TABLE and self.status == False:
            self.translation = translation
            self.status = status  # 翻译完成，设置状态为True

    def get_origianl_to_string(self):
        """获取原始内容的字符串表示
         :return: 原始内容的字符串表示
         """
        return json.dumps(self.original.values.tolist(),ensure_ascii=False)

