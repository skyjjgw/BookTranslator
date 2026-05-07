class RagService:
    """
    第三阶段最小版知识库服务示例。
    先理解接口形态，再替换为真实向量数据库实现。
    """

    def __init__(self, vector_store, retriever, llm):
        self.vector_store = vector_store
        self.retriever = retriever
        self.llm = llm

    def index_document(self, chunks):
        for chunk in chunks:
            self.vector_store.add_text(chunk)

    def ask(self, question: str):
        contexts = self.retriever.search(question, top_k=3)
        prompt = self._build_prompt(contexts, question)
        return self.llm.invoke(prompt)

    def _build_prompt(self, contexts, question):
        joined_context = "\n".join(contexts)
        return (
            "你是企业文档问答助手。\n"
            f"已检索到的上下文如下：\n{joined_context}\n"
            f"用户问题：{question}\n"
            "请严格根据上下文回答，不知道就明确说不知道。"
        )
