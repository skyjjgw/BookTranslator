# 第二阶段：OCR 与复杂文档解析

## 阶段目标

让项目不只支持“可复制文本 PDF”，还支持：

- 扫描件
- 图片文档
- 截图
- 复杂版式文档

业务上，这一步非常关键，因为企业真实文档很多不是标准 PDF。

## 你需要学习的知识

- OCR 基础
- PaddleOCR 或 PP-Structure
- PyMuPDF 基础
- 文本块、表格块、图片块的版面识别
- 文档清洗与噪声处理

## 当前项目的不足

你现在主要依赖：

- `pdfplumber.extract_text()`
- `pdfplumber.extract_tables()`

这对标准 PDF 有效，但对扫描件支持弱。

## 这一步新增的业务价值

有了 OCR 后，你就能把项目从“PDF翻译工具”升级成：

- 企业文档数字化处理系统

因为你不仅能翻译，还能把原本不可检索的扫描资料转成结构化数据。

## 这一步建议新增的模块

```text
app/
  services/ocr_service.py
  services/parser_service.py
  pipelines/document_router.py
```

## 处理流程建议

1. 先判断文档是否是扫描件
2. 如果是普通 PDF，走 `pdfplumber`
3. 如果是扫描件或图片，走 OCR
4. 把结果统一整理为：
   - 文本块
   - 表格块
   - 图片块

## 你要新增的代码重点

- 新增 `OCRService`
- 新增 `ParserService`
- 新增 `DocumentRouter`

其中 `DocumentRouter` 用来判断文档走哪条链路，这个非常像 Agent 的第一步“路由决策”。

## 最小实现建议

先别追求太复杂，按下面顺序做：

1. 只支持图片 OCR
2. 再支持扫描 PDF 转图片
3. 最后做版面分区

## 这一阶段的结果

完成后，你的项目就可以写成：

- 支持 PDF 与扫描件统一解析的智能文档处理系统

## 这一阶段适合写进简历的话

- 设计 OCR 与版面解析链路，补齐扫描件与图片文档处理能力，实现文本、表格等内容块的统一抽取与后续大模型处理。
