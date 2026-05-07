from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate




class Model:
        def create_llm(self):
                print("初始化模型")



        def make_prompt(self):
                """创建提示词"""
                system_prompt = """你是一个翻译专家，输入的是{source_language}的文本内容，你需要将其翻译成{target_language}，翻译后的语言是{target_language}。请确保翻译后的文本内容准确、流畅，并且符合目标语言的语法和文化习惯。"""
                system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt)
                human_message_prompt = HumanMessagePromptTemplate.from_template("{text}")

                return ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])




