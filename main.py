from src.PDFtoImages import convert_pdf_to_jpg
from src.GetPageNo import GetPageNo
from src.RagClass import Rag
from src.ChromaSearcher import MarkdownSearcher
import os
import shutil


# ConvertedImagesディレクトリのクリーンアップ
output_folder = "./ConvertedImages"
if os.path.exists(output_folder):
    # ディレクトリ内のすべてのファイルを削除
    shutil.rmtree(output_folder)
    # ディレクトリを再作成
    os.makedirs(output_folder)
else:
    # ディレクトリが存在しない場合は新規作成
    os.makedirs(output_folder)

#今はとりあえずここで指定している。本当はstreamlitかなんかで実装
pdf_path = "data/BSA071000 法定定期自主検査実施要領.pdf"

#pdfの名前を抽出(できているのかは不明。時間あるときに確認)
pdf_name = pdf_path.split("/")[-1].split(".")[0]

print(f"PDF名: {pdf_name}")
#queryを取得(ここはstreamlitかなんかで実装)
query = "性能検査を社内で行えない設備" 
#マークダウンをqueryに基づいてHybrid(もしくはベクトル)検索
searcher = MarkdownSearcher()

# PDFファイル名に基づいて適切なMarkdownファイルを選択
file_name = searcher.get_markdown_file_name(pdf_name)
print(f"検索対象ファイル: {file_name}")

# コレクション名を取得
collection_name = searcher.get_collection_name(file_name)
    
    # 検索実行
results = searcher.search(
        collection_name,
        query,
        n_results=3,
        alpha=0.1  # セマンティック検索をより重視
)

#Hybrid検索結果から該当ページを取得
pageNo = GetPageNo(file_name,results[0]['content'])

#該当ページ前後の画像を取得(最終的にはページを指定)
convert_pdf_to_jpg(pdf_path, "./ConvertedImages")

#該当ページ前後の画像と付近のマークダウンでRAG検索  
rag = Rag()
response = rag.process(file_name, "./ConvertedImages", pageNo, query)

#RAG検索結果を出力
print(response)



