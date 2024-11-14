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
from src.AllProcessor import allProcessor
def load_test_cases(json_path):
    """テストケースをJSONファイルから読み込む"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    
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
        result = allProcessor(pdf_path, case['question'])
        # print(f"期待される回答: {case['answer']}")
        # print(f"実際の回答: {response}")
        results.append({
            "テストケース": case['question'],
            "期待されるページ番号": case['page'],
            "実際のページ番号": result["pageNos"],
            "期待される回答": case['answer'],
            "実際の回答": result["response"]
        })
    save_results_to_json("法定定期自主検査実施要領_results.json", results)
def test_press_machine():
    """動力プレス機械安全基準のテスト"""
    test_cases = load_test_cases("test/動力プレス機械安全基準：通則.json")
    pdf_path = r"data/BSA120200 動力プレス機械安全基準：通則.pdf"
    results = []
    for case in test_cases:
        print(f"\nテストケース: {case['question']}")
        result = allProcessor(pdf_path, case['question'])
        results.append({
            "テストケース": case['question'],
            "期待されるページ番号": case['page'],
            "実際のページ番号": result["pageNos"],
            "期待される回答": case['answer'],
            "実際の回答": result["response"]
        })
    save_results_to_json("動力プレス機械安全基準_results.json", results)
if __name__ == "__main__":
    print("法定定期自主検査実施要領のテスト開始")
    test_legal_inspection()
    print("\n動力プレス機械安全基準のテスト開始")
    test_press_machine()