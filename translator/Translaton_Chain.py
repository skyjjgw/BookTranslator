from BookTranslator.ai_model.model import Model
from BookTranslator.book.content import ContentType
from BookTranslator.utils.log_utils import log

class TranslationChain:
    """翻译链，负责将文本内容翻译成指定语言
    """
    def __init__(self, model):
       # 提示词 模型
       self.langchain = model.make_prompt() | model.create_llm()
    def run(self,content,source_language,target_language):
        """翻译文本内容
        :param content: 需要翻译的文本内容
        :param source_language: 原语言
        :param target_language: 目标语言
        :return: 翻译后的文本内容
        """
        text = ''
        result = ''



        if content.content_type == ContentType.TEXT:
            text = f"请按照要求翻译以下文本内容：{content.original}"
            result = self.langchain.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': text
            })
            log.info(result.content)
            return result.content, True
        elif content.content_type ==ContentType.TABLE:
            text = f"请按照要求翻译以下内容，严格以json 二维数据格式返回（例如[[“行1列1”,“行1列2”],[“行2列1”,“行2列2”]]]）：不要包含markdown格式，只返回json格式。{content.original.to_string()}"
            result = self.langchain.invoke({
                'source_language': source_language,
                'target_language': target_language,
                'text': text
            })
            log.info(result.content)
            return result,True
