import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from typing import List

# 環境変数を読み込む
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Rag:
    def query_openai(self, markdown: str, images: List[str], query: str) -> str:
        """
        OpenAIのAPIを使用してクエリに対する回答を生成
        
        Args:
            markdown (str): 入力テキスト
            images (List[str]): base64エンコードされた画像のリスト
            query (str): 質問テキスト
            
        Returns:
            str: OpenAIからの応答
        """
        try:
            # メッセージリストの作成
            messages: List[ChatCompletionMessageParam] = [
                ChatCompletionSystemMessageParam(
                    role="system",
                    content="あなたは与えられた文書と画像に基づいて質問に答えるアシスタントです。"
                ),
                ChatCompletionUserMessageParam(
                    role="user",
                    content=f"以下の文書と画像に基づいて質問に答えてください。\n\n文書：{markdown}\n\n質問：{query}"
                )
            ]

            # 画像をメッセージに追加
            for base64_image in images:
                messages.append(ChatCompletionUserMessageParam(
                    role="user",
                    content=f"データ画像:\n{base64_image}"
                ))

            response = client.chat.completions.create(
                model="gpt-4",  # モデル名を修正
                messages=messages,
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
            pageNo (int): ページ番号
            query (str): 質問テキスト
            
        Returns:
            str: OpenAIからの応答
        """
        try:
            # マークダウンファイルを読み込み
            with open(markdownPath, "r", encoding="utf-8") as f:
                markdown = f.read()
            
            # フォルダ内のJPGファイルをカウント
            jpg_count = len([f for f in os.listdir(imagePath) if f.endswith('.jpg')])
            images = []

            # 指定されたページの画像を読み込み
            if 1 <= pageNo <= jpg_count:
                image_path = os.path.join(imagePath, f"{pageNo}.jpg")
                if os.path.exists(image_path):
                    with open(image_path, "rb") as image_file:
                        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                        images.append(base64_image)
        
            # OpenAIに質問を投げる
            return self.query_openai(markdown, images, query)
            
        except Exception as e:
            return f"処理中にエラーが発生しました: {str(e)}"