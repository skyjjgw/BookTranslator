# BookTranslator

BookTranslator is an LLM-powered document translation and reconstruction project. It currently supports PDF text and table extraction, content-type-aware translation routing, and export to both PDF and Markdown.

At its current stage, the project works as a document translation pipeline. In the next iterations, it is intended to evolve into a more business-oriented **Enterprise Document Processing Agent** with OCR, knowledge retrieval, service APIs, and workflow orchestration.

## Highlights

- Extracts both text blocks and table content from PDF files
- Supports model switching between `DeepSeek` and `OpenAI`
- Routes different content types through different processing logic
- Exports translated results to both `PDF` and `Markdown`
- Provides a reusable foundation for a future enterprise document agent

## Current Capabilities

The current processing flow includes:

1. Load configuration and command-line arguments
2. Initialize the selected LLM
3. Parse PDF text and tables
4. Route each content block through the translation chain
5. Write translated content back into the document object
6. Export the final result as PDF or Markdown

## Architecture

### 1. Bootstrap and Configuration

- Entry point: `main.py`
- Configuration center: `utils/project_config.py`
- CLI parsing: `utils/argument_utils.py`

Responsibilities:

- Load project settings from `config.yaml`
- Allow CLI arguments to override the config file
- Select the model implementation dynamically based on `model_type`

### 2. Model Abstraction Layer

Directory: `ai_model/`

Main files:

- `model.py`: shared prompt template and model abstraction
- `deepseek_model.py`: DeepSeek integration
- `openai_model.py`: OpenAI integration

Responsibilities:

- Hide provider-specific model differences
- Build a unified LangChain-based model call pipeline

### 3. Document Parsing and Translation Layer

Directory: `translator/`

Core files:

- `pdf_parser.py`
- `book_translation.py`
- `Translaton_Chain.py`
- `file_writer.py`

Responsibilities:

- Use `pdfplumber` to extract text and tables from PDF files
- Convert page content into structured content blocks
- Apply different prompting logic for text and tables
- Rebuild translated content as PDF or Markdown

### 4. Content Abstraction Layer

Directory: `book/`

Main files:

- `book.py`
- `pages.py`
- `content.py`

Responsibilities:

- Define the `Book / Page / Content` object model
- Support content type enums for text, image, and table
- Leave room for future OCR and multimodal extensions

## Project Structure

```text
BookTranslator/
  ai_model/              # Model abstraction layer
  book/                  # Document object model
  translator/            # Parsing, translation, and export pipeline
  utils/                 # Config, logging, and utility helpers
  fonts/                 # Fonts for PDF output
  logs/                  # Runtime logs
  test/                  # Sample files and generated outputs
  enterprise_doc_agent_plan/  # Learning and upgrade roadmap
  config.yaml            # Runtime configuration
  main.py                # Project entry point
  README.md              # Project documentation
```

## Tech Stack

- Python
- LangChain
- DeepSeek / OpenAI API
- pdfplumber
- pandas
- reportlab
- loguru
- PyYAML

## Quick Start

### 1. Install Dependencies

Create a virtual environment first, then install the required packages:

```bash
pip install -r requirements.txt
```

If you prefer manual installation, the main dependencies are:

```bash
pip install langchain langchain-community pdfplumber pandas reportlab loguru pyyaml openpyxl matplotlib
```

### 2. Configure the Project

Edit `config.yaml`:

```yaml
model_type: "deepseek"
model_name: "deepseek-chat"
input_file: "test/test_table.pdf"
file_format: "md"
source_language: "en"
target_language: "zh"
pages: null
apikey: "your_api_key"
```

Field descriptions:

- `model_type`: model provider, currently `deepseek` or `openai`
- `model_name`: concrete model name
- `input_file`: input PDF path
- `file_format`: output format, `pdf` or `md`
- `source_language`: source language
- `target_language`: target language
- `pages`: page limit, `null` means process all pages
- `apikey`: provider API key

### 3. Run the Project

```bash
python main.py
```

You can also override configuration values from the command line:

```bash
python main.py --model_type deepseek --model_name deepseek-chat --input_file test/test_table.pdf --file_format md --source_language en --target_language zh
```

## Output

The output file name is automatically generated from the source file name:

- `xxx_translator.pdf`
- `xxx_translator.md`

Current output support includes:

- paragraph translation
- table translation to Markdown table format
- translated PDF reconstruction

## Known Limitations

This project is still in an early stage and currently has several limitations:

- Mainly supports standard PDF files, with weak support for scanned documents
- Runs as a local script rather than a production service
- Does not yet include a terminology base or RAG-powered QA
- Does not yet provide a task queue, workflow tracking, or evaluation pipeline
- Does not yet have a formal test suite

## Roadmap

This repository will gradually evolve into an **Enterprise Document Processing Agent** with the following capabilities:

### Phase 1: Service Layer

- Add FastAPI-based upload and result query APIs
- Support batch tasks and basic task status management

### Phase 2: OCR and Complex Document Parsing

- Support scanned PDFs and image documents
- Add OCR and layout-aware parsing

### Phase 3: RAG and Document QA

- Index processed documents into a knowledge base
- Add semantic retrieval
- Support document-grounded question answering and summarization

### Phase 4: Workflow and Evaluation

- Introduce LangGraph-based orchestration
- Add async jobs, retries, and human review hooks
- Add quality metrics and token cost tracking

For a detailed learning and upgrade plan, see:

- `enterprise_doc_agent_plan/`

## Potential Business Use Cases

After future upgrades, the project can be adapted to:

- internal enterprise knowledge document processing and search
- foreign trade material translation and restructuring
- bidding, proposal, and government documentation workflows
- training material digitization and document QA

## Suggested Next Steps

If you want to keep improving this repository as a resume-ready project, the recommended order is:

1. Finalize `requirements.txt`
2. Add `FastAPI` and turn the script into a service
3. Add OCR support
4. Add knowledge retrieval and QA
5. Add evaluation metrics and automated tests

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
