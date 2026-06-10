from .model import Model
from langchain.chat_models import init_chat_model
from BookTranslator.utils.log_utils import log

class OpenAIModel(Model):
    def __init__(self, model,api_key):
        self.model_name = model
        self.api_key = api_key


    def create_llm(self):
        log.info(f"初始化 OpenAI 模型: {self.model_name}")
        return init_chat_model(
            model=self.model_name,
            api_key=self.api_key
        )

if __name__ == '__main__':
    pass
