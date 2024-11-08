from chromadb import PersistentClient
from typing import List
import os
import re
class MarkdownIndexer:
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = PersistentClient(path=db_path)
        
    def chunk_markdown(self, markdown_text: str, max_chunk_size: int = 3000) -> List[str]:
        """
        Markdownテキストをチャンクに分割
        
        Args:
            markdown_text (str): 入力テキスト
            chunk_size (int): チャンクサイズ
            
        Returns:
            List[str]: チャンク化されたテキストのリスト
        """
        chunks: List[str] = []
        current_chunk: List[str] = []
        current_size = 0
        
        # セクション単位で分割
        sections = re.split(r'(?=^#|\n#)', markdown_text)
        
        for section in sections:
            section_size = len(section)
            if section_size > max_chunk_size:
                # テーブルは分割しない
                if '|' in section:
                    chunks.append(section)
                    continue
                
                # 段落単位で分割
                paragraphs = section.split('\n\n')
                temp_chunk = []
                temp_size = 0
                
                for para in paragraphs:
                    if temp_size + len(para) > max_chunk_size:
                        if temp_chunk:
                            chunks.append('\n\n'.join(temp_chunk))
                        temp_chunk = [para]
                        temp_size = len(para)
                    else:
                        temp_chunk.append(para)
                        temp_size += len(para) + 2
                        
                if temp_chunk:
                    chunks.append('\n\n'.join(temp_chunk))
            else:
                chunks.append(section)
                
        return chunks
    
    def index_markdown(self, markdown_path: str, collection_name: str):
        """
        Markdownファイルをインデックス化してChromaDBに保存
        """
        try:
            # コレクションの取得または作成
            collection = self.client.get_or_create_collection(collection_name)
            
            # Markdownファイルの読み込み
            with open(markdown_path, 'r', encoding='utf-8') as file:
                markdown_text = file.read()
            
            # テキストのチャンク化
            chunks = self.chunk_markdown(markdown_text)
            
            # チャンクをDBに追加
            collection.add(
                documents=chunks,
                ids=[f"chunk_{i}" for i in range(len(chunks))]
            )
            
            return True
            
        except Exception as e:
            print(f"インデックス化エラー: {e}")
            return False

# 使用例
if __name__ == "__main__":
    indexer = MarkdownIndexer()
    indexer.index_markdown("./MarkDowns/PressMachine.md", "press_collection")