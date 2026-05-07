from .file_writer import FileWriter

from .Translaton_Chain import TranslationChain
from .pdf_parser import parse_pdf
from BookTranslator.utils.log_utils import log



class PDFTranslator:
    """
PDF翻译器，负责将PDF内容翻译成指定语言
    """
    def __init__(self, model):
        self.book = None
        self.chain = TranslationChain(model)
        self.writer = FileWriter(self.book)



    def book_translator(self,file_path,source_language,target_language,out_file_format="pdf",output_file_path=None, pages=None):
        """
        翻译PDF内容
        :param file_path: PDF文件路径
        :param source_language: 原语言
        :param target_language: 目标语言
        :param file_format: 输出文件格式
        :param output_file_path: 输出文件路径
        :return: 翻译后的PDF文件路径
        """
        self.book = parse_pdf(file_path,pages)
        self.writer.book = self.book
        # 遍历每个页面
        for page_index, page in enumerate(self.book.pages):
            # 遍历每个页面的内容
            for content_index, content in enumerate(page.content):
                translator_text, status = self.chain.run(content, source_language, target_language)
                content.set_translation(translator_text.content if hasattr(translator_text, 'content') else translator_text, status)
                log.debug(f"翻译之后的内容：{translator_text.content if hasattr(translator_text, 'content') else translator_text}，翻译状态：{status}")

                self.book.pages[page_index].content[content_index].set_translation(translator_text.content if hasattr(translator_text, 'content') else translator_text, status)


        self.writer.save_book(output_file_path, out_file_format)



