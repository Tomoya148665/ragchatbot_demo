import json
#import pytest
import sys
import os

# プロジェクトのルートディレクトリをPYTHONPATHに追加
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.PDFtoImages import convert_pdf_to_jpg
from src.GetPageNo import GetPageNo
from src.RagClass import Rag
from src.ChromaSearcher import MarkdownSearcher
import os
import shutil

def load_test_cases(json_path):
    """テストケースをJSONファイルから読み込む"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_search_test(pdf_path, query):
    """検索処理を実行する"""
    # ConvertedImagesディレクトリのクリーンアップ
    output_folder = "./ConvertedImages"
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    # PDFの名前を抽出
    pdf_name = pdf_path.split("/")[-1].split(".")[0]

    # 検索実行
    searcher = MarkdownSearcher()
    # PDFファイル名に基づいて適切なMarkdownファイルを選択
    file_path = searcher.get_markdown_file_name(pdf_name)
    print(f"検索対象ファイル: {file_path}")
    print(f"検索クエリ: {query}")

    # コレクション名を取得
    collection_name = searcher.get_collection_name(file_path)
        
    # 検索実行
    results = searcher.search(
        collection_name,
        query,
        n_results=3,
        alpha=0.1  # セマンティック検索をより重視
    )


    # ページ番号取得
    pageNo = GetPageNo(results[0]['content'])

    # 画像変換
    convert_pdf_to_jpg(pdf_path, output_folder)

    # RAG検索
    rag = Rag()
    response = rag.process(file_path, output_folder, pageNo, query)

    return response

def save_results_to_json(filename, results):
    """結果をJSONファイルに保存する"""
    output_dir = "./test/outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

def test_legal_inspection():
    """法定定期自主検査実施要領のテスト"""
    test_cases = load_test_cases("test/法定定期自主検査実施要領.json")
    pdf_path = "data/BSA071000 法定定期自主検査実施要領.pdf"
    results = []

    for case in test_cases:
        print(f"\nテストケース: {case['question']}")
        response = run_search_test(pdf_path, case['question'])
        # print(f"期待される回答: {case['answer']}")
        # print(f"実際の回答: {response}")
        results.append({
            "テストケース": case['question'],
            "期待される回答": case['answer'],
            "実際の回答": response
        })
    
    save_results_to_json("法定定期自主検査実施要領_results.json", results)

def test_press_machine():
    """動力プレス機械安全基準のテスト"""
    test_cases = load_test_cases("test/動力プレス機械安全基準：通則.json")
    pdf_path = "data/BSA120200 動力プレス機械安全基準：通則.pdf"
    results = []

    for case in test_cases:
        print(f"\nテストケース: {case['question']}")
        response = run_search_test(pdf_path, case['question'])
        results.append({
            "テストケース": case['question'],
            "期待される回答": case['answer'],
            "実際の回答": response
        })
    
    save_results_to_json("動力プレス機械安全基準_results.json", results)

if __name__ == "__main__":
    print("法定定期自主検査実施要領のテスト開始")
    test_legal_inspection()
    
    print("\n動力プレス機械安全基準のテスト開始")
    test_press_machine()