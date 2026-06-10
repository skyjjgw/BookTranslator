from BookTranslator.translator.book_translation import PDFTranslator
from utils.project_config import ProjectConfig
from ai_model.openai_model import OpenAIModel
from ai_model.deepseek_model import DeepSeekModel
from memory.memory_store import MemoryStore




def main():
    config = ProjectConfig()
    config.initialize()


    if config.model_type == "openai":
        model = OpenAIModel(config.model_name, config.apikey)
    elif config.model_type == "deepseek":
        model = DeepSeekModel(config.model_name, config.apikey)
    else:
        raise ValueError(f"不支持的模型类型: {config.model_type}")


    memory_store = MemoryStore(
        db_path=config.memory_db_path,
        enabled=config.memory_enabled,
        domain=config.memory_domain,
    )

    #初始化一个翻译器
    translator = PDFTranslator(
        model,
        memory_store=memory_store,
        resume_from_checkpoint=config.resume_from_checkpoint,
    )
    translator.book_translator(
        file_path=config.input_file,
        source_language=config.source_language,
        target_language=config.target_language,
        output_file_path='test',
        out_file_format=config.file_format,
        pages=config.pages,
    )

if __name__ == "__main__":
    main()
