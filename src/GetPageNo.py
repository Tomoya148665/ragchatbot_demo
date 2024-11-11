def GetPageNo(ansText: str) -> int:
    """
    テキストからページ番号を抽出
    
    Args:
        text (str): ページのテキスト
        
    Returns:
        int: 抽出したページ番号
    """
    # "# Page " で始まる行からページ番号を抽出
    if ansText.startswith("# Page "):
        try:
            # "# Page " の後の数字を取得
            page_num = int(ansText.split("# Page ")[1].split("\n")[0])
            print(page_num)
            return page_num
        except:
            return -1
    return -1