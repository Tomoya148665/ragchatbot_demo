from docling.document_converter import DocumentConverter

source = "./pdf/Kensa.pdf"

def pdf_to_markdown(pdf_path: str) -> str:
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown() 

def refference_part(markdown: str) -> str:
    return markdown.split("## 参考文献")[0]

print(refference_part(pdf_to_markdown(source)))
    

