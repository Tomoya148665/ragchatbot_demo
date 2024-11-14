def GetPageNo(ansTexts: list[str]) -> list[int]:
    """
    テキストからページ番号を抽出
    
    Args:
        text (str): ページのテキスト
        
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
    page_nos = []
    for Text in ansTexts:
        # "# Page "で始まる行を探す
        lines = Text.split('\n')
        for line in lines:
            if line.startswith('# Page '):
                try:
                    # "# Page "の後の数字を抽出して整数に変換
                    page_no = int(line.replace('# Page ', '').strip())
                    page_nos.append(page_no)
                except ValueError:
                    continue
    
    return page_nos