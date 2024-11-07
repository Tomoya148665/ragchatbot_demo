from src.MarkDownReader import MarkDownReader
from src.GetPageNo import search_text_in_pages

# 使用例:
content = MarkDownReader().read_markdown("./MarkDowns/pdf_plumber_combined.md")
results = search_text_in_pages(content, "アセチレン")
print(f"Found on pages: {results}")