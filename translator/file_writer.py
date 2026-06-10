import json
import os
from matplotlib import colors
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
        output_file_path = self._resolve_output_path(output_file_path, ".pdf")
        log.debug(f'pdf原文件路径是{self.book.file_path}翻译之后的路径是{output_file_path}')

        self._register_font()
        style = ParagraphStyle('MiSans', fontName='MiSans', fontSize=12)
        doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter)
        pdf_data = []

        for page in self.book.pages:
            for content in page.content:
                if content.content_type == ContentType.TEXT and content.translation:
                    pdf_data.append(Paragraph(text=str(content.translation), style=style))
                elif content.content_type == ContentType.TABLE:
                    table_rows = self._parse_table_rows(content.translation)
                    if not table_rows:
                        continue
                    table_style = TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'MiSans'),
                        ('FONTSIZE', (0, 0), (-1, 0), 14),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('FONTNAME', (0, 1), (-1, -1), 'MiSans'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ])
                    table = Table(data=table_rows)
                    table.setStyle(table_style)
                    pdf_data.append(table)

            if page != self.book.pages[-1]:
                pdf_data.append(PageBreak())

        doc.build(pdf_data)
        log.info(f"翻译后的PDF文件已保存到：{output_file_path}")
        return output_file_path




    def save_book_md(self, output_file_path):
        """保存翻译后的PDF内容到Markdown文件
        :param output_file_path: 输出文件路径
        :return: None
        """
        output_file_path = self._resolve_output_path(output_file_path, ".md")
        log.debug(f'md原文件路径是{self.book.file_path}翻译之后的路径是{output_file_path}')

        with open(output_file_path, 'w', encoding='utf-8') as md_file:
            for page in self.book.pages:
                for content in page.content:
                    if content.content_type == ContentType.TEXT and content.translation:
                        md_file.write(str(content.translation) + '\n\n')
                    elif content.content_type == ContentType.TABLE:
                        rows = self._parse_table_rows(content.translation)
                        if rows and len(rows) > 0:
                            header_row = rows[0]
                            body_row = rows[1:]

                            header = '| ' + " | ".join(str(cell) for cell in header_row) + " |\n"
                            tr = "|" + "|".join(["---"] * len(header_row)) + "|\n"

                            t_body = ''
                            for row in body_row:
                                t_body += '| ' + ' | '.join(str(cell) for cell in row) + ' |\n'
                            md_file.write(header + tr + t_body + '\n')

                if page != self.book.pages[-1]:
                    md_file.write('\n---\n\n')
        log.info(f"翻译后的Markdown文件已保存到：{output_file_path}")
        return output_file_path

    def _resolve_output_path(self, output_target, extension):
        source_root = os.path.splitext(self.book.file_path)[0]
        default_output = f"{source_root}_translator{extension}"

        if not output_target:
            return default_output

        if os.path.isdir(output_target) or not os.path.splitext(output_target)[1]:
            os.makedirs(output_target, exist_ok=True)
            file_name = os.path.basename(source_root) + f"_translator{extension}"
            return os.path.join(output_target, file_name)

        os.makedirs(os.path.dirname(output_target) or ".", exist_ok=True)
        return output_target

    def _register_font(self):
        font_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "fonts",
            "MiSans-Light.ttf",
        )
        pdfmetrics.registerFont(TTFont('MiSans', font_path))

    def _parse_table_rows(self, translation):
        try:
            if isinstance(translation, str):
                parsed = json.loads(translation)
            else:
                parsed = translation.values.tolist()
        except Exception as e:
            log.error(f"解析表格数据失败: {e}")
            return []

        if not isinstance(parsed, list):
            return []
        return [[("" if cell is None else str(cell)) for cell in row] for row in parsed if isinstance(row, list)]






