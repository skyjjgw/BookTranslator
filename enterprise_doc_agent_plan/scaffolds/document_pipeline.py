from dataclasses import dataclass


@dataclass
class DocumentTask:
    file_path: str
    source_language: str
    target_language: str
    output_format: str = "md"


class DocumentPipeline:
    """
    这是从你当前 BookTranslator 演进到企业文档 Agent 时最值得先抽象的类。
    它的职责不是直接写业务，而是把处理流程固定下来。
    """

    def __init__(self, parser, translator, writer):
        self.parser = parser
        self.translator = translator
        self.writer = writer

    def run(self, task: DocumentTask):
        parsed_book = self.parser.parse(task.file_path)

        for page in parsed_book.pages:
            for content in page.content:
                translated = self.translator.translate(
                    content=content,
                    source_language=task.source_language,
                    target_language=task.target_language,
                )
                content.set_translation(translated, True)

        return self.writer.write(parsed_book, task.output_format)
