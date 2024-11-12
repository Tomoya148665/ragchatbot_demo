def GetPageNo(file_path: str, answer_text: str) -> int:
    """
    Markdownファイル内でテキストを検索し、該当するページ番号を返す
    
    Args:
        file_path (str): Markdownファイルのパス
        answer_text (str): 検索したいテキスト
    
    Returns:
        int: 検索テキストが見つかったページ番号（見つからない場合は-1）
    """
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        print(f"ファイルが見つかりません: {file_path}")
        return -1
    """
    
    # "# Page "で始まる行を探す
    lines = answer_text.split('\n')
    for line in lines:
        if line.startswith('# Page '):
            try:
                # "# Page "の後の数字を抽出して整数に変換
                page_no = int(line.replace('# Page ', '').strip())
                print(f"ページ番号: {page_no}")
                return page_no
            except ValueError:
                continue
    
    return page_no