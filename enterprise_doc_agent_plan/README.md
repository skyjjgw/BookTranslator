# 企业智能文档处理 Agent 学习与改造路线

这个目录不是替换你现在的 `BookTranslator`，而是告诉你如何基于当前项目逐步升级出一个更偏业务、更像 AI Agent 的新项目。

## 目标项目

建议你后续把项目包装为：

- 企业智能文档处理 Agent

一句话定义：

- 面向企业资料流转与知识管理场景，完成文档解析、术语增强翻译、结构化抽取、知识入库与问答检索。

## 当前项目能保留什么

你现在的项目已经有下面这些可复用能力：

- 配置中心：`utils/project_config.py`
- 模型封装：`ai_model/`
- 文档解析：`translator/pdf_parser.py`
- 内容抽象：`book/content.py`
- 翻译链：`translator/Translaton_Chain.py`
- 输出重建：`translator/file_writer.py`

这些代码可以视为新项目的第一版 `document pipeline`。

## 你接下来要补的能力

只靠“翻译 PDF”业务价值偏弱，所以要继续补下面四层能力：

1. 服务化
2. OCR 与复杂文档解析
3. RAG 知识检索与问答
4. 工作流编排、评测和任务队列

## 学习顺序

请按下面顺序学习和改造：

1. [01_service_and_upload.md](file:///D:/BaiduNetdiskDownload/BookTranslator/enterprise_doc_agent_plan/phases/01_service_and_upload.md)
2. [02_ocr_and_parsing.md](file:///D:/BaiduNetdiskDownload/BookTranslator/enterprise_doc_agent_plan/phases/02_ocr_and_parsing.md)
3. [03_rag_and_qa.md](file:///D:/BaiduNetdiskDownload/BookTranslator/enterprise_doc_agent_plan/phases/03_rag_and_qa.md)
4. [04_workflow_and_eval.md](file:///D:/BaiduNetdiskDownload/BookTranslator/enterprise_doc_agent_plan/phases/04_workflow_and_eval.md)

## 代码脚手架

为了让你不只停留在文档，我还额外放了 3 个最小脚手架：

- [fastapi_app.py](file:///D:/BaiduNetdiskDownload/BookTranslator/enterprise_doc_agent_plan/scaffolds/fastapi_app.py)
- [document_pipeline.py](file:///D:/BaiduNetdiskDownload/BookTranslator/enterprise_doc_agent_plan/scaffolds/document_pipeline.py)
- [rag_service.py](file:///D:/BaiduNetdiskDownload/BookTranslator/enterprise_doc_agent_plan/scaffolds/rag_service.py)

它们不是完整项目，而是后续你新增代码时最先可以抄的结构。

## 建议的新项目结构

你后续可以把真正的新项目单独开成下面这样的结构：

```text
enterprise-doc-agent/
  app/
    api/
    core/
    services/
    pipelines/
    schemas/
    agents/
    storage/
  data/
  tests/
  docs/
```

## 每阶段你会学到什么

- 第一阶段：把脚本升级成接口服务
- 第二阶段：让系统支持扫描件、图片和复杂版面
- 第三阶段：把文档变成知识库，支持问答
- 第四阶段：让系统更像真正的 Agent，支持编排、评测和异步任务

## 最终简历包装方向

等你做完前 3 个阶段，这个项目就可以包装成：

- 企业智能文档处理 Agent：支持 PDF/扫描件解析、术语增强翻译、结构化重建、知识入库与语义问答

## 你现在最该做的事

先做第一阶段，不要一上来就堆太多技术：

- 学 `FastAPI`
- 学文件上传接口
- 学如何把你现有的 `PDFTranslator` 封装成服务层
- 学如何返回任务结果
