from operator import itemgetter
from typing import Any, Dict, List
import os

import pdfplumber


def extract_contents(page: pdfplumber.page.Page) -> List[Dict[str, Any]]:
    """
    PDFページから重複しないテキストおよび表データを抽出する。

    Args:
        page (pdfplumber.page.Page): PDFのページオブジェクト。

    Returns:
        List[Dict[str, Any]]: テキストや表データを含むリスト。
    """
    contents = []
    tables = page.find_tables()

    # テーブルに含まれないすべてのテキストデータを抽出
    non_table_content = page
    for table in tables:
        non_table_content = non_table_content.outside_bbox(table.bbox)

    for line in non_table_content.extract_text_lines():
        contents.append({'top': line['top'], 'text': line['text']})

    # すべての表データを抽出
    for table in tables:
        contents.append({'top': table.bbox[1], 'table': table})

    # 行を上部位置でソート
    contents = sorted(contents, key=itemgetter('top'))

    return contents

def sanitize_cell(cell: Any) -> str:
    """
    セルの内容を整理する。

    Args:
        cell (Any): セルのデータ。

    Returns:
        str: 整理されたセルデータ。
    """
    if cell is None:
        return ""
    else:
        # すべての種類の空白を削除し、文字列であることを保証
        return ' '.join(str(cell).split())

def save_to_single_markdown(filepath: str, all_pages_contents: List[List[Dict[str, Any]]]) -> None:
    """
    すべてのページの内容を1つのMarkdownファイルに保存する。

    Args:
        filepath (str): 保存先のMarkdownファイルパス。
        all_pages_contents (List[List[Dict[str, Any]]]): 各ページの内容を含むリスト。
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        for page_number, contents in enumerate(all_pages_contents, start=1):
            file.write(f'# Page {page_number}\n\n')

            for content in contents:
                if 'text' in content:
                    # テキスト内容を段落として書き込む
                    file.write(f"{content['text']}\n\n")
                elif 'table' in content:
                    table = content['table']
                    unsanitized_table = table.extract()  # 表オブジェクトからデータを抽出
                    sanitized_table = [[sanitize_cell(cell) for cell in row] for row in unsanitized_table]
                    # ヘッダーセパレーターを作成
                    header_separator = '|:--' * len(sanitized_table[0]) + ':|\n'
                    # テーブルデータをMarkdown形式に変換
                    for i, row in enumerate(sanitized_table):
                        md_row = '| ' + ' | '.join(row) + ' |\n'
                        file.write(md_row)
                        # 最初の行（ヘッダー行）の後にヘッダーセパレーターを追加
                        if i == 0:
                            file.write(header_separator)
                    # テーブルの後にセパレーターを追加（任意）
                    file.write('\n---\n\n')

            file.write('\n')

    print(f"All pages have been written to {filepath}")

def process_pdf(pdf_path: str, output_filepath: str) -> None:
    """
    PDFの各ページを処理して1つのMarkdownファイルに保存する。

    Args:
        pdf_path (str): 処理するPDFファイルのパス。
        output_filepath (str): 保存するMarkdownファイルのパス。
    """
    all_pages_contents: List[List[Dict[str, Any]]] = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines = extract_contents(page)
            all_pages_contents.append(lines)

    # すべての内容を1つのMarkdownファイルに保存
    save_to_single_markdown(output_filepath, all_pages_contents)

# メインの実行部分
if __name__ == "__main__":
    # 絶対パスを使用
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "..", "data", "BSA120200 動力プレス機械安全基準：通則.pdf")
    output_filepath = os.path.join(current_dir, "..", "MarkDowns", "PressMachine.md")

    # 処理を実行
    process_pdf(pdf_path, output_filepath)
