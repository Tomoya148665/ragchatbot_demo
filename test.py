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
    collection_name = 'pdf_plumber_combined_collection'
    
    # 検索実行
    results = searcher.search(
        collection_name, #ここでコレクションを直接指定
        query
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