from src.PDFtoImages import convert_pdf_to_jpg
from src.GetPageNo import GetPageNo
from src.RagClass import Rag
from src.ChromaSearcher import MarkdownSearcher
import os
import shutil

def allProcessor(pdf_path: str, query: str, ForUI:bool = False):
    """
    PDFドキュメントに対するクエリを処理する関数
    
    Args:
        pdf_path (str): PDFファイルのパス
        query (str): 検索クエリ
        ForUI (bool): UI表示フラグ
    Returns:
        str: RAG検索の結果
    """
    try:
        # ConvertedImagesディレクトリのセットアップ
        output_folder = "./ConvertedImages"
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)

        # PDFファイル名の抽出
        pdf_name = pdf_path.split("/")[-1].split(".")[0]
        print(f"PDF名: {pdf_name}")

        # マークダウン検索の設定と実行
        searcher = MarkdownSearcher()
        file_path = searcher.get_markdown_file_name(pdf_name)
        print(f"検索対象ファイル: {file_path}")
        
        collection_name = searcher.get_collection_name(file_path)
        results = searcher.search(collection_name, query)


        # ページ番号の取得
        pageContents = [result['content'] for result in results]
        pageNos = sorted(GetPageNo(pageContents))

        # PDF画像変換
        convert_pdf_to_jpg(pdf_path, output_folder)

        # RAG検索実行
        rag = Rag()
        response = rag.process(file_path, output_folder, pageNos, query)

        ragResult = {
            "pageNos": pageNos,
            "response": response
        }
        if ForUI:
            return {
                "ChromaResult": results,
                "RAGResult": ragResult
            }
        else:
            return ragResult

    except Exception as e:
        return f"エラーが発生しました: {str(e)}"

if __name__ == "__main__":
    # 使用例
    pdf_path = "data/BSA071000 法定定期自主検査実施要領.pdf"
    query = "火薬類とはどのようなもののこと？"
    
    response = allProcessor(pdf_path, query)
    print(response)