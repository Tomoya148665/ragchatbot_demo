from chromadb import PersistentClient
from typing import List
import os
import re
import openai
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class MarkdownIndexer:
    def __init__(self, db_path: str= "./chroma_db"):#= chroma_dbのあるパスを指定.入力ファイル名によってパスを変更
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
    
    def embed_text(self, text: str) -> List[float]:
        """
        OpenAIの`text-embedding-ada-002`モデルを使用してテキストをベクトル化
        
        Args:
            text (str): ベクトル化するテキスト
            
        Returns:
            List[float]: ベクトル化されたテキスト
        """
        response = openai.Embedding.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response['data'][0]['embedding']

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
            # チャンクをベクトル化
            embeddings = [self.embed_text(chunk) for chunk in chunks]
            
            
            # チャンクをDBに追加
            collection.add(
                documents=chunks,
                embeddings=embeddings,
                ids=[f"chunk_{i}" for i in range(len(chunks))]
            )
            
            return True
            
        except Exception as e:
            print(f"インデックス化エラー: {e}")
            return False
        
    def index_multiple_markdowns(self, file_mappings: dict):
        print("インデックス化開始")

        for file_path, collection_name in file_mappings.items():
            #既存のコレクションがあれば削除
            try:
                self.client.delete_collection(collection_name)
                print(f"既存のコレクション {collection_name} を削除しました")
            except: pass

            #新しくインデックス化
            success = self.index_markdown(file_path, collection_name)
            if success:
                print(f"インデックス化完了: {file_path} → {collection_name}")
                collection = self.client.get_collection(collection_name)
                print(f"コレクション {collection_name} を取得しました")
            else:
                print(f"インデックス化失敗: {file_path} → {collection_name}")
        print("インデックス化完了")

# 使用例
if __name__ == "__main__":
    indexer = MarkdownIndexer()
    file_mappings = {
        "./MarkDowns/PressMachine.md": "PressMachine_collection",
        "./MarkDowns/pdf_plumber_combined.md": "pdf_plumber_combined_collection"
    }
    indexer.index_multiple_markdowns(file_mappings)

    # 利用可能なコレクションを取得
    collections = indexer.client.list_collections()
    print("\n利用可能なコレクション:")
    for collection in collections:
        print(collection.name)
