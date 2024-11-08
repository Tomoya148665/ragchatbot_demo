def GetPageNo(file_path: str, answer_text: str) -> int:
    """
    Markdownファイル内でテキストを検索し、該当するページ番号を返す
    
    Args:
        file_path (str): Markdownファイルのパス
        answer_text (str): 検索したいテキスト
    
    Returns:
        int: 検索テキストが見つかったページ番号（見つからない場合は-1）
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
        return -1
    
    # 結果を格納する変数を初期化
    found_page = -1  # デフォルト値を設定
    
    # ページごとに分割 ("# Page" をセパレータとして使用)
    pages = content.split("# Page ")
    
    # 各ページをチェック
    for i, page_content in enumerate(pages[1:], 1):  # 最初の空要素をスキップ
        # 検索クエリが現在のページに含まれているかチェック
        if answer_text in page_content:
            found_page = i
            break
    
    if found_page == -1:
        print(f"テキストが見つかりませんでした: {answer_text}")
    else:
        print(f"テキストが見つかったページ: {found_page}")
    
    return found_page