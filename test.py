from src.ChromaSearcher import MarkdownSearcher

def test_search_and_page():
    # 初期化
    searcher = MarkdownSearcher()
    
    # テストケース
    pdf_name = "BSA120200 動力プレス機械安全基準：通則"
    query = "光線式安全装置の構造において故障したときどのようになっていないといけない？"
    
    # PDFファイル名に基づいて適切なMarkdownファイルを選択
    file_name = searcher.get_markdown_file_name(pdf_name)
    print(f"\n検索対象ファイル: {file_name}")
    if pdf_name == "BSA120200 動力プレス機械安全基準：通則":
        collection_name = "PressMachine_collection"
    else:
        collection_name = "pdf_plumber_combined_collection"

    
    # 検索実行
    results = searcher.search(
        collection_name, #ここでコレクションを直接指定
        query,
        n_results=5
    )
    
    # 検索結果の確認
    if results:
        for result in results:
            print("\n検索結果の内容:")
            print("=" * 50)
            print("semantic_score:", result['semantic_score'])
            print("keyword_score:", result['keyword_score'])
            print("score:", result['score'])
            print("=" * 50)
            
            # content内のページ番号を確認
            content_lines = result['content'].split('\n')
            print("\n最初の数行:")
            for line in content_lines[:5]:
                print(f"行: {repr(line)}")
    else:
        print("検索結果が見つかりませんでした")

if __name__ == "__main__":
    test_search_and_page()