from docx import Document
import sys

def read_docx(file_path):
    try:
        doc = Document(file_path)
        for i, para in enumerate(doc.paragraphs):
            print(f"[{i}] {para.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_docx(r"C:\Users\skyjj\Desktop\就业+考研\详细路线.docx")