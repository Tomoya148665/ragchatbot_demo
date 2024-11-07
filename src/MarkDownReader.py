class MarkDownReader:
    def __init__(self):
        pass

    def read_markdown(self, file_path: str) -> str:
        """
        Markdownファイルを読み込み、文字列として返す
        
        Args:
            file_path (str): Markdownファイルのパス
            
        Returns:
            str: Markdownファイルの内容
            
        Raises:
            FileNotFoundError: ファイルが見つからない場合
            Exception: その他のエラーが発生した場合
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
            
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        except Exception as e:
            raise Exception(f"ファイルの読み込み中にエラーが発生しました: {str(e)}")

