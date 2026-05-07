from BookTranslator.translator.book_translation import PDFTranslator
from utils.project_config import ProjectConfig
from ai_model.openai_model import OpenAIModel
from ai_model.deepseek_model import DeepSeekModel
from utils.argument_utils import ArgumentUtils




def main():
    config = ProjectConfig()
    config.initialize()


    if config.model_type == "openai":
        model = OpenAIModel(config.model_name, config.apikey)
    elif config.model_type == "deepseek":
        model = DeepSeekModel(config.model_name, config.apikey)
    else:
        raise ValueError(f"不支持的模型类型: {config.model_type}")


    #初始化一个翻译器
    translator = PDFTranslator(model)
    translator.book_translator(file_path=config.input_file,source_language=config.source_language,target_language=config.target_language,output_file_path='test',out_file_format=config.file_format,pages=config.pages)

if __name__ == "__main__":
    main()