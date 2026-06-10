import json
import re

from BookTranslator.ai_model.model import Model
from BookTranslator.book.content import ContentType
from BookTranslator.utils.log_utils import log

class TranslationChain:
    """翻译链，负责将文本内容翻译成指定语言
    """
    def __init__(self, model):
       # 提示词 模型
       self.langchain = model.make_prompt() | model.create_llm()
    def run(self,content,source_language,target_language,memory_context=""):
        """翻译文本内容
        :param content: 需要翻译的文本内容
        :param source_language: 原语言
        :param target_language: 目标语言
        :return: 翻译后的文本内容
        """
        if content.content_type == ContentType.TEXT:
            text = f"请按照要求翻译以下文本内容：{content.original}"
            if memory_context:
                text = f"{memory_context}\n\n{text}"
            result = self.langchain.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': text
            })
            log.info(result.content)
            return result.content, True
        elif content.content_type ==ContentType.TABLE:
            text = (
                "请翻译以下表格内容，并严格返回 JSON 二维数组。"
                "不要返回 Markdown，不要返回解释，不要添加代码块。"
                "示例格式：[[\"col1\",\"col2\"],[\"value1\",\"value2\"]]。\n"
                f"原始表格：{content.get_origianl_to_string()}"
            )
            if memory_context:
                text = f"{memory_context}\n\n{text}"
            result = self.langchain.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': text
            })
            sanitized_table = self._sanitize_table_result(result.content)
            log.info(sanitized_table)
            return sanitized_table, True

    def _sanitize_table_result(self, raw_text):
        if not raw_text:
            return "[]"

        cleaned = raw_text.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"(\[\s*\[.*\]\s*\])", cleaned, flags=re.DOTALL)
            if not match:
                log.warning("表格翻译结果不是合法 JSON，已回退为空数组")
                return "[]"
            try:
                parsed = json.loads(match.group(1))
            except json.JSONDecodeError:
                log.warning("表格翻译结果清洗失败，已回退为空数组")
                return "[]"

        if not isinstance(parsed, list):
            log.warning("表格翻译结果不是二维数组，已回退为空数组")
            return "[]"

        normalized_rows = []
        for row in parsed:
            if isinstance(row, list):
                normalized_rows.append(["" if cell is None else str(cell) for cell in row])
            else:
                normalized_rows.append([str(row)])
        return json.dumps(normalized_rows, ensure_ascii=False)
