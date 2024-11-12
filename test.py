from src.ChromaSearcher import MarkdownSearcher

def test_search_and_page():
    # 初期化
    searcher = MarkdownSearcher()
    
    # テストケース
    pdf_name = "BSA071000 法定定期自主検査実施要領"
    query = "性能検査を社内で行えない設備"
    
    # PDFファイル名に基づいて適切なMarkdownファイルを選択
    file_name = searcher.get_markdown_file_name(pdf_name)
    print(f"\n検索対象ファイル: {file_name}")
    
    # 検索実行
    results = searcher.search_by_file(
        file_name,
        query,
        n_results=3,
        alpha=0.1
    )
    
    # 検索結果の確認
    if results:
        print("\n検索結果の内容:")
        print("=" * 50)
        print(results[0]['content'])
        print("=" * 50)
        
        # content内のページ番号を確認
        content_lines = results[0]['content'].split('\n')
        print("\n最初の数行:")
        for line in content_lines[:5]:
            print(f"行: {repr(line)}")
    else:
        print("検索結果が見つかりませんでした")

if __name__ == "__main__":
    test_search_and_page()