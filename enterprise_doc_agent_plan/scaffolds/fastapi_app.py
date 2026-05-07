from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel


app = FastAPI(title="Enterprise Document Agent")


class ProcessResponse(BaseModel):
    message: str
    saved_path: str
    next_step: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/documents/upload", response_model=ProcessResponse)
async def upload_document(file: UploadFile = File(...)):
    # 第一步先做最小上传接口，后续再接真正的处理流水线
    saved_path = f"data/uploads/{file.filename}"
    content = await file.read()
    with open(saved_path, "wb") as f:
        f.write(content)

    return ProcessResponse(
        message="文件上传成功",
        saved_path=saved_path,
        next_step="在 service 层调用现有 PDFTranslator 进行解析和输出",
    )
