# 第一阶段：服务化与文件上传

## 阶段目标

把你现在的命令行翻译脚本，升级成一个可以对外提供服务的最小系统。

业务上，这一步对应的是：

- 用户上传文档
- 系统自动处理
- 返回输出文件地址或任务结果

## 这一步为什么重要

企业不会直接用命令行脚本，第一步必须先服务化。

只有先把项目做成服务，后面才好继续接：

- 前端页面
- 任务队列
- 多用户使用
- 批量处理

## 你需要学习的知识

- FastAPI 基础
- `POST /upload` 文件上传
- `GET /task/{id}` 结果查询
- Pydantic 数据校验
- 服务层与路由层分离

## 你现有代码如何复用

可以直接复用下面这些模块：

- `translator/book_translation.py`
- `translator/pdf_parser.py`
- `translator/Translaton_Chain.py`
- `translator/file_writer.py`
- `ai_model/`

## 这一步建议新增的代码

建议你在新项目里新增这些文件：

```text
app/
  main.py
  api/document.py
  services/document_service.py
  schemas/document.py
```

## 每个文件负责什么

- `app/main.py`
  启动 FastAPI 应用
- `app/api/document.py`
  定义上传、查询接口
- `app/services/document_service.py`
  调用你现有的文档处理链路
- `app/schemas/document.py`
  定义请求和响应结构

## 你要做的具体操作

1. 先安装 FastAPI 和 Uvicorn
2. 把现有 `PDFTranslator` 封装成服务方法
3. 新增上传接口，把文件保存到本地目录
4. 返回处理结果路径
5. 用 Postman 或 Apifox 测试接口

## 最小可交付能力

这一阶段完成后，你的项目要能做到：

- 接收 PDF 文件
- 调用现有翻译链路
- 输出 PDF 或 Markdown
- 通过接口返回处理状态

## 建议新增的第一批代码

优先新增：

- `FastAPI` 应用入口
- 上传接口
- 文档服务层

不要急着加：

- Redis
- Celery
- 前端
- 向量数据库

## 这一阶段适合写进简历的话

- 将命令行文档翻译脚本升级为基于 FastAPI 的文档处理服务，支持文件上传、任务执行与结果返回，为后续业务化部署提供接口基础。
