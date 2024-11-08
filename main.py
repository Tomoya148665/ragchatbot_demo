from src.pdf_plumber import process_pdf
from src.PDFtoImages import PDFtoImages
from src.GetPageNo import GetPageNo
from src.RagClass import Rag

#pdfをマークダウン化
process_pdf(pdf_path, output_filepath)

#queryを取得

#マークダウンをqueryに基づいてHybrid(もしくはベクトル)検索

#Hybrid検索結果から該当ページを取得
GetPageNo(Markdown,answer_text)

#該当ページ前後の画像を取得(最終的にはページを指定)
PDFtoImages(pdf_path, output_folder)

#該当ページ前後の画像と付近のマークダウンでRAG検索  
rag = Rag()
rag.process(markdownPath, imagePath, pageNo, query)

#RAG検索結果を出力

