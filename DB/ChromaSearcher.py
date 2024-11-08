from chromadb import PersistentClient
from typing import List, Dict

class MarkdownSearcher:
    def __init__(self, db_path: str = "./chroma_db"):
        self.client = PersistentClient(path=db_path)
    
    def search(self, collection_name: str, query: str, n_results: int = 1) -> List[Dict]:
        """
        インデックス化されたMarkdownから検索を実行
        
        Args:
            collection_name (str): コレクション名
            query (str): 検索クエリ
            n_results (int): 返す結果の数
            
        Returns:
            List[Dict]: 検索結果のリスト
        """
        try:
            collection = self.client.get_collection(collection_name)
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # 結果を整形
            formatted_results = []
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    'content': doc,
                    'score': results['distances'][0][i] if 'distances' in results else None
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"検索エラー: {e}")
            return []

# 使用例
if __name__ == "__main__":
    searcher = MarkdownSearcher()
    results = searcher.search("press_collection", "動力プレス機械新設の届け出期日")
    for i, result in enumerate(results, 1):
        print(f"\n結果 {i}:")
        print(f"内容: {result['content']}")  
        if result['score'] is not None:
            print(f"スコア: {result['score']}")