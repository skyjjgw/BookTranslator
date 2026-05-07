
from matplotlib import colors
from openpyxl.styles.table import TableStyle
from reportlab.lib import pagesizes
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak

from BookTranslator.book.content import ContentType
from BookTranslator.utils.log_utils import log



from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


class FileWriter:
    """
    文件写入器，负责将翻译后的PDF内容写入文件
    """
    def __init__(self, book):
        self.book = book

    def save_book(self, output_file_path=None, file_format="pdf"):
        """
        保存翻译后的PDF内容到文件
        :param output_file_path: 输出文件路径
        :param file_format: 输出文件格式，默认为pdf
        :return: None
        """
        if file_format.lower() == "pdf":
            return self.save_book_pdf(output_file_path)
        elif file_format.lower() == "md":
            return self.save_book_md(output_file_path)
        else:
            log.warning("当前文文件不支持")
            return ''
    def save_book_pdf(self, output_file_path):
        """
        保存翻译后的PDF内容到PDF文件
        :param output_file_path: 输出文件路径
        :return: None
        """
        print(output_file_path,type(output_file_path))
        if  output_file_path is not None:


            subfix = self.book.file_path[self.book.file_path.rindex("."):]
            print(subfix)
            output_file_path = self.book.file_path.replace(subfix, f"_translator.pdf")
            log.debug(f'pdf原文件路径是{self.book.file_path}翻译之后的路径是{output_file_path}')

            #先注册字
            pdfmetrics.registerFont(TTFont('MiSans', r'D:\BaiduNetdiskDownload\BookTranslator\fonts\MiSans-Light.ttf'))


            #创建pdf字体样式

            style =  ParagraphStyle('MiSans', fontName='MiSans', fontSize=12)
            #创建一个pdf文档

            doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter)
            pdf_data = []



            for page in self.book.pages:
                for content in page.content:
                    # if content.status:
                        if content.content_type == ContentType.TEXT:
                            #写一个段落
                            pdf_data.append(Paragraph(text=content.translation, style=style))
                        elif content.content_type == ContentType.TABLE:
                            #写一个表格
                            table_style = TableStyle([
                                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # 表头背景色
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # 表头文字颜色
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # 所有单元格内容居中对齐
                                ('FONTNAME', (0, 0), (-1, 0), 'MiSans'),  # 表头字体
                                ('FONTSIZE', (0, 0), (-1, 0), 14),  # 表头字体大小: 14pt
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # 表头底部内边距
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # 表体背景色
                                ('FONTNAME', (0, 1), (-1, -1), 'MiSans'),  # 表体字体
                                ('GRID', (0, 0), (-1, -1), 1, colors.black),  # 表格网格线: 1pt
                            ])
                            import json
                            table_data = json.loads(content.translation) if isinstance(content.translation, str) else content.translation.values.tolist()
                            table = Table(data=table_data)
                            table.setStyle(table_style)
                            pdf_data.append(table)

                if page != self.book.pages[-1]:  # 如果不是最后一页，添加分页符
                 pdf_data.append(PageBreak())

            doc.build(pdf_data)
            log.info(f"翻译后的PDF文件已保存到：{output_file_path}")
            return output_file_path




    def save_book_md(self, output_file_path):
        """保存翻译后的PDF内容到Markdown文件
        :param output_file_path: 输出文件路径
        :return: None
        """
        if output_file_path is not None:
            subfix = self.book.file_path[self.book.file_path.rindex("."):]
            output_file_path = self.book.file_path.replace(subfix, f"_translator.md")
            log.debug(f'md原文件路径是{self.book.file_path}翻译之后的路径是{output_file_path}')

            with open(output_file_path, 'w', encoding='utf-8') as md_file:
                for page in self.book.pages:
                    for content in page.content:
                        if content.content_type == ContentType.TEXT:
                            md_file.write(str(content.translation) + '\n\n')
                        elif content.content_type == ContentType.TABLE:
                            import json
                            try:
                                rows = json.loads(content.translation) if isinstance(content.translation, str) else content.translation.values.tolist()
                            except Exception as e:
                                log.error(f"解析表格数据失败: {e}")
                                rows = []
                                
                            if rows and len(rows) > 0:
                                header_row = rows[0]
                                body_row = rows[1:]

                                # 组装markdown表格字符串
                                header = '| ' + " | ".join(str(cell) for cell in header_row) + " |\n"
                                tr = "|" + "|".join(["---"] * len(header_row)) + "|\n"
                                
                                t_body = ''
                                for row in body_row:
                                    t_body += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
                                md_file.write(header + tr + t_body + '\n')

                    if page != self.book.pages[-1]:  # 如果不是最后一页，添加分页符
                        md_file.write('\n---\n\n')
            log.info(f"翻译后的Markdown文件已保存到：{output_file_path}")
            return output_file_path






