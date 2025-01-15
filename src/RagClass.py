import os
import base64
from dotenv import load_dotenv
from openai import OpenAI
from typing import List

# 環境変数を読み込む
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Rag:
    def query_openai(self, markdownList: list[str], images: List[str], query: str) -> str:
        """
        OpenAIのAPIを使用してクエリに対する回答を生成
        """
        try:
            # メッセージコンテンツの作成
            messages_content = [
                {
                    "type": "text",
                    "text": f"以下の文書と画像にだけ基づいて質問に答えてください。その際、リスト、テーブルや図表から必ず抜けた情報がないように読み取るようにしてください。\n\n質問：{query}\n\n文書："
                }
            ]
            for markdown in markdownList:
                messages_content.append({
                    "type": "text",
                    "text": markdown
                })

            # 画像をメッセージに追加
            for base64_image in images:
                messages_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                })

            # メッセージの作成
            messages = [
                {
                    "role": "system",
                    "content": "あなたは与えられた文書と画像にだけ基づいて質問に答えるアシスタントです。過不足なく回答してください。"
                },
                {
                    "role": "user",
                    "content": messages_content
                }
            ]

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"

    def process(self, markdownPath: str, imagePath: str, pageNos: list[int], query: str) -> str:
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
            filtered_markdown:list[str]=[] # ページ番号が指定されている場合のマークダウンを格納するリスト
            # マークダウンファイルを読み込み
            with open(markdownPath, "r", encoding="utf-8") as f:
                markdown = f.read()
            # ページ番号が指定されている場合、そのページの内容のみを抽出
            if pageNos is not None:
                pages = markdown.split("# Page ")
                for pageno in pageNos:
                    for page in pages:
                        # 各ページの先頭の数字を取得
                        if page.strip():  # 空でないページのみ処理
                            try:
                                page_num = int(page.split('\n')[0])
                                if page_num == pageno:
                                    filtered_markdown.append(page)
                            except ValueError:
                                continue
            
            # フォルダ内のJPGファイルをカウント
            jpg_count = len([f for f in os.listdir(imagePath) if f.endswith('.jpg')])
            images = []

            # 指定されたページの画像を読み込み
            for pageNo in sorted(pageNos):
                print(f"pageno:{pageNo}")
                if 1 <= pageNo <= jpg_count:
                    image_path = os.path.join(imagePath, f"{pageNo}.jpg")
                    if os.path.exists(image_path):
                        with open(image_path, "rb") as image_file:
                            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
                            images.append(base64_image)
            # デバッグ出力を追加
            print("マークダウンの先頭部分:")
            for md in filtered_markdown:
                # 最初の50文字を出力（必要に応じて文字数を調整）
                preview = md[:10] + "..." if len(md) > 50 else md
                print(f"- {preview}")
        
            # OpenAIに質問を投げる
            return self.query_openai(filtered_markdown, images, query)
            
        except Exception as e:
            return f"処理中にエラーが発生しました: {str(e)}"