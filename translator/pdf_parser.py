import pdfplumber

from BookTranslator.book.book import Book
from BookTranslator.book.content import Content, ContentType, TableContent
from BookTranslator.book.pages import Page
from BookTranslator.utils.exception import PageOutOfRangeError
from BookTranslator.utils.log_utils import log

def parse_pdf(file_path,pages):
    """
    解析PDF文件，提取文本和图片
    :param file_path: PDF文件路径
    :return: Book对象，包含页面内容和图片信息
    param pages: 需要解析的页数，如果为None则解析所有页面
    """

    book = Book(file_path)
    with pdfplumber.open(file_path) as pdf:
        if pages and pages >len(pdf.pages):
            # 如果pages参数大于PDF总页数，解析所有页面
            raise PageOutOfRangeError(len(pdf.pages), pages)
        # 没传
        if pages is None:
            #[page1, page2, page3, ...]
            pages_arr = pdf.pages
        else:
            pages_arr = pdf.pages[:pages]

        for pdf_page in pages_arr:
            page = Page()# 创建一个新的页面对象
            # 提取文本
            raw_text = pdf_page.extract_text()
            # 提取表格
            tables = pdf_page.extract_tables() or []

            # 在raw_text删掉表格内容
            #三维数组
            if raw_text:
                for table in tables:
                    for row in table:
                        for cell in row:
                            if cell:
                                raw_text = raw_text.replace(cell, "")

            if raw_text:
                lines = raw_text.splitlines()
                clear_lines = [line for line in lines if line.strip() != ""]
                clear_text = "\n".join(clear_lines)
                # 将清洗后的文本添加到页面内容中
                text_content=Content(content_type=ContentType.TEXT, original="\n".join(clear_lines))
                page.add_content(text_content)# 将文本内容添加到页面内容中
                log.debug(f"提取文本内容：{clear_text}")

            if tables:# 提取表格内容
                for table in tables:# 遍历每个表格
                    table_content = TableContent(content_type=ContentType.TABLE, original=table)
                    page.add_content(table_content)# 将表格内容添加到页面内容中
                    log.debug(f"提取表格内容：{table}")
            book.add_page(page)# 将页面添加到书籍中

        return book
if __name__ == "__main__":
    book = parse_pdf(r"D:\BaiduNetdiskDownload\BookTranslator\test\test.pdf", None)
    print(book)




