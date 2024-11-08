from src.RagClass import Rag

rag = Rag()
print(rag.process("./MarkDowns/pdf_plumber_combined.md", "./ConvertedImages", 5, "性能検査を社内で実施できない設備を全て教えてください"))
