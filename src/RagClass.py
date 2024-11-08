import os
from openai import OpenAI
import base64

class Rag:
    def __init__(self):
        # OpenAI APIクライアントの初期化
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")  # 環境変数からAPIキーを取得
        )

    def query_openai(self, markdown: str, images: list[str], query: str) -> str:
        """
        OpenAIのAPIを使用してクエリに対する回答を生成
        
        Args:
            markdown (str): 入力テキスト
            images (list[str]): base64エンコードされた画像のリスト
            query (str): 質問テキスト
            
        Returns:
            str: OpenAIからの応答
        """
        try:
            # メッセージコンテンツの作成
            messages_content = [
                {
                    "type": "text",
                    "text": f"以下の文書と画像に基づいて質問に答えてください。\n\n文書：{markdown}\n\n質問：{query}"
                }
            ]

            # 画像をメッセージに追加
            for base64_image in images:
                messages_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })

            response = self.client.chat.completions.create(
                model="gpt-4o",  # または必要なモデル
                messages=[
                    {
                        "role": "system",
                        "content": "あなたは与えられた文書と画像に基づいて質問に答えるアシスタントです。"
                    },
                    {
                        "role": "user",
                        "content": messages_content
                    }
                ],
                max_tokens=500
            )
            return response.choices[0].message.content
            
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"

    def process(self, markdownPath: str, imagePath: str, pageNo: int, query: str) -> str:
        """
        マークダウンと画像を処理してOpenAIに質問する
        
        Args:
            markdownPath (str): マークダウンファイルのパス
            imagePath (str): 画像フォルダのパス
            query (str): 質問テキスト
            
        Returns:
            str: OpenAIからの応答
        """
        # マークダウンファイルを読み込み
        markdown = open(markdownPath, "r", encoding="utf-8").read()
        
        # フォルダ内のJPGファイルをカウント
        jpg_count = len([f for f in os.listdir(imagePath) if f.endswith('.jpg')])
        images = []

        for i in range(jpg_count):
            # 画像を読み込んでbase64エンコード
            if i+1 == pageNo:
                with open(os.path.join(imagePath, f"{i+1}.jpg"), "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                    images.append(base64_image)
        
        # OpenAIに質問を投げる
        response = self.query_openai(markdown, images, query)
        
        return response

# 使用例:
"""
rag = Rag()
response = rag.process(
    markdownPath="path/to/markdown.md",
    imagePath="path/to/images",
    query="あなたの質問"
)
print(response)
"""