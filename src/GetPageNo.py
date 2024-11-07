def search_text_in_pages(content: str, search_query: str) -> list[int]:
    """
    PDFコンテンツ内でテキストを検索し、該当するページ番号のリストを返す
    
    Args:
        content (str): PDFから抽出したテキストコンテンツ
        search_query (str): 検索したいテキスト
    
    Returns:
        list[int]: 検索テキストが見つかったページ番号のリスト
    """
    # 結果を格納するリスト
    found_pages = []
    
    # ページごとに分割 ("# Page" をセパレータとして使用)
    pages = content.split("# Page ")
    
    # 各ページをチェック
    for i, page_content in enumerate(pages[1:], 1):  # 最初の空要素をスキップ
        # 検索クエリが現在のページに含まれているかチェック
        if search_query in page_content:
            found_pages.append(i)
    
    return found_pages


