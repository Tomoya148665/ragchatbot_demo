from src.AllProcessor import allProcessor
if __name__ == "__main__":
    # 使用例
    pdf_path = "data/BSA120200 動力プレス機械安全基準：通則.pdf"
    query = "光線式安全装置の構造において故障したときどのようになっていないといけない？"
    
    result = allProcessor(pdf_path, query)
    print(result["response"])