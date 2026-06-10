from .file_writer import FileWriter

from .Translaton_Chain import TranslationChain
from .pdf_parser import parse_pdf
from BookTranslator.utils.log_utils import log



class PDFTranslator:
    """
PDF翻译器，负责将PDF内容翻译成指定语言
    """
    def __init__(self, model, memory_store=None, resume_from_checkpoint=False):
        self.book = None
        self.chain = TranslationChain(model)
        self.writer = FileWriter(self.book)
        self.memory_store = memory_store
        self.resume_from_checkpoint = resume_from_checkpoint



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
                checkpoint = self._load_checkpoint(file_path, page_index, content_index, source_language, target_language)
                if checkpoint:
                    content.set_translation(checkpoint, True)
                    self.book.pages[page_index].content[content_index].set_translation(checkpoint, True)
                    continue

                cached_translation = self._load_cached_translation(content, source_language, target_language)
                if cached_translation:
                    content.set_translation(cached_translation, True)
                    self.book.pages[page_index].content[content_index].set_translation(cached_translation, True)
                    self._save_checkpoint(file_path, page_index, content_index, source_language, target_language, "completed", cached_translation)
                    continue

                memory_context = self._build_memory_context(content, source_language, target_language)
                try:
                    translator_text, status = self.chain.run(
                        content,
                        source_language,
                        target_language,
                        memory_context=memory_context,
                    )
                    content.set_translation(translator_text, status)
                    log.debug(f"翻译之后的内容：{translator_text}，翻译状态：{status}")
                    self.book.pages[page_index].content[content_index].set_translation(translator_text, status)
                    self._save_translation_memory(content, translator_text, source_language, target_language)
                    self._save_checkpoint(file_path, page_index, content_index, source_language, target_language, "completed", translator_text)
                except Exception:
                    self._save_checkpoint(file_path, page_index, content_index, source_language, target_language, "failed")
                    raise

        self.writer.save_book(output_file_path, out_file_format)

    def _load_checkpoint(self, file_path, page_index, content_index, source_language, target_language):
        if not self.memory_store or not self.resume_from_checkpoint:
            return None
        checkpoint = self.memory_store.get_checkpoint(
            file_path,
            page_index,
            content_index,
            source_language,
            target_language,
        )
        if checkpoint and checkpoint["status"] == "completed" and checkpoint["translation"]:
            log.info(f"命中断点记忆: page={page_index}, content={content_index}")
            return checkpoint["translation"]
        return None

    def _load_cached_translation(self, content, source_language, target_language):
        if not self.memory_store:
            return None
        cached_translation = self.memory_store.get_cached_translation(content, source_language, target_language)
        if cached_translation:
            log.info("命中翻译记忆，跳过模型调用")
        return cached_translation

    def _build_memory_context(self, content, source_language, target_language):
        if not self.memory_store:
            return ""
        return self.memory_store.build_memory_context(content, source_language, target_language)

    def _save_translation_memory(self, content, translated_text, source_language, target_language):
        if self.memory_store:
            self.memory_store.save_translation_memory(content, translated_text, source_language, target_language)

    def _save_checkpoint(self, file_path, page_index, content_index, source_language, target_language, status, translation=None):
        if self.memory_store:
            self.memory_store.save_checkpoint(
                file_path,
                page_index,
                content_index,
                source_language,
                target_language,
                status,
                translation,
            )



