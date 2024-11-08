from chromadb import PersistentClient
from typing import List, Dict
import os

class MarkdownSearcher:
    def __init__(self, db_path: str = "./chroma_db"): #= "./chroma_db"のあるパスを指定
        self.client = PersistentClient(path=db_path)
        self.collections_mapping = {
            "PressMachine": "press_collection",
            "pdf_plumber_combined": "plumber_collection"
        }

    def get_markdown_file_name(self, pdf_name: str) -> str:
        """
        PDFファイル名からMarkdownファイル名を取得
        
        Args:
            pdf_name (str): PDFファイル名
            
        Returns:
            str: Markdownファイル名
        """
        # PDFファイル名とMarkdownファイル名のマッピング
        pdf_to_markdown = {
            "BSA071000 法定定期自主検査実施要領": "pdf_plumber_combined",
            "BSA120200 動力プレス機械安全基準：通則": "PressMachine"
        }
        
        # マッピングからMarkdownファイル名を取得
        for pdf_pattern, markdown_name in pdf_to_markdown.items():
            if pdf_pattern in pdf_name:
                return f"./MarkDowns/{markdown_name}.md"
        
        raise ValueError(f"未対応のPDFファイルです: {pdf_name}\n"
                        f"対応しているPDF: {list(pdf_to_markdown.keys())}")
    
    def get_collection_name(self, file_name: str) -> str:
        # 拡張子とパスを除去してベースファイル名を取得
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        collection_name = f"{base_name.lower()}_collection"
        # コレクションが存在するか確認
        available_collections = [c.name for c in self.client.list_collections()]
        if collection_name not in available_collections:
            raise ValueError(f"コレクションが見つかりません: {collection_name}\n"
                           f"利用可能なコレクション: {available_collections}")
        
        return collection_name
    
    def search_by_file(self, file_name: str, query: str, n_results: int = 3,
                      alpha: float = 0.5) -> List[Dict]:
        """
        ファイル名を指定して検索を実行
        
        Args:
            file_name (str): 検索対象のファイル名
            query (str): 検索クエリ
            n_results (int): 返す結果の数
            alpha (float): キーワード検索の重み
            
        Returns:
            List[Dict]: 検索結果のリスト
        """
        try:
            collection_name = self.get_collection_name(file_name)
            print(f"検索対象コレクション: {collection_name}")
            return self.search(collection_name, query, n_results, alpha)
        except Exception as e:
            print(f"検索エラー: {e}")
            return []

    
    def search(self, collection_name: str, query: str, n_results: int = 3,
               alpha: float = 0.5) -> List[Dict]:
        """
        インデックス化されたMarkdownから検索を実行
        
        Args:
            collection_name (str): コレクション名
            query (str): 検索クエリ
            n_results (int): 返す結果の数
            alpha (float): キーワード検索の重み（0.0〜1.0）
            
        Returns:
            List[Dict]: 検索結果のリスト
        """
        try:
            collection = self.client.get_collection(collection_name)
            
            # セマンティック検索の実行
            results = collection.query(
                query_texts=[query],
                n_results=n_results * 2,  # より多くの候補を取得
                include=['documents', 'distances']
            )
            
            if not results['documents'][0]:
                print("検索結果が見つかりませんでした。")
                return []
                
            merged_results = []
            for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
                # キーワードスコアの計算
                keyword_score = self.calculate_keyword_score(doc, query)
                
                # セマンティックスコアの計算（距離を類似度に変換）
                semantic_score = 1.0 - (distance / max(results['distances'][0]))
                
                # 最終スコアの計算
                final_score = (keyword_score * alpha + semantic_score * (1-alpha))
                
                merged_results.append({
                    'content': doc,
                    'score': round(final_score, 3),
                    'keyword_score': round(keyword_score, 3),
                    'semantic_score': round(semantic_score, 3)
                })
            
            # スコアでソート
            merged_results.sort(key=lambda x: x['score'], reverse=True)
            return merged_results[:n_results]
                
        except Exception as e:
            print(f"検索エラー: {e}")
            print(f"利用可能なコレクション: {[c.name for c in self.client.list_collections()]}")
            return []
    
    def extract_keywords(self, query: str) -> str:
        """
        クエリから重要なキーワードを抽出
        
        Args:
            query (str): 検索クエリ
            
        Returns:
            str: 抽出されたキーワード（助詞区切り）
        """
        # 助詞などの不要な語を除去
        stop_words = {'は', 'の', 'が', 'を', 'に', 'へ', 'で', 'や', 'と', 'から'}
        for stop_word in stop_words:
            query = query.replace(stop_word, ' ')
        words = [w.strip() for w in query.split()]
        keywords = list(dict.fromkeys(words)) # 重複を削除
        return ' '.join(keywords)
    
    def calculate_keyword_score(self, text: str, query: str) -> float:
        """
        キーワードマッチングスコアを計算（改善版）
        
        Args:
            text (str): 検索対象テキスト
            query (str): 検索クエリ
            
        Returns:
            float: キーワードスコア（0.0〜1.0）
        """
        keywords = self.extract_keywords(query)
        if not keywords:
            return 0.0
        
        # キーワードを分割
        keyword_list = keywords.split()
        matches = 0
        
        for keyword in keyword_list:
            # 部分一致のチェック
            if keyword.lower() in text.lower():
                matches += 1
        
        # スコアの正規化（0〜1の範囲に）
        score = matches / (len(keyword_list) )  # 1.5はボーナススコアを考慮
        return min(1.0, score)  # 1.0を超えないように

# 使用例
if __name__ == "__main__":
    searcher = MarkdownSearcher()
    print("検索を開始します...")
    
    # 利用可能なコレクションを表示
    collections = searcher.client.list_collections()
    print(f"利用可能なコレクション: {[c.name for c in collections]}")

    file_name = "./MarkDowns/pdf_plumber_combined.md"
    query = "性能検査を社内で行えない設備"
    
    # 検索実行
    results = searcher.search_by_file(
        file_name, 
        query,
        n_results=3,
        alpha=0.1  # セマンティック検索をより重視
    )
    
    if results:
        for i, result in enumerate(results, 1):
            print(f"\n結果 {i}:")
            print(f"内容: {result['content']}")
            print(f"総合スコア: {result['score']}")
            print(f"キーワードスコア: {result['keyword_score']}")
            print(f"セマンティックスコア: {result['semantic_score']}")
    else:
        print("検索結果が見つかりませんでした。")