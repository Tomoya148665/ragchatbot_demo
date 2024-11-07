import fitz  # PyMuPDFライブラリのインポート
import os

def convert_pdf_to_jpg(pdf_file, output_folder):
    """
    特定のPDFファイルをページごとにJPEGファイルとして保存する。

    Parameters:
    - pdf_file: 変換するPDFファイルのパス。
    - output_folder: 画像を保存するフォルダのパス。
    """
    # 出力フォルダが存在しない場合、作成する
    os.makedirs(output_folder, exist_ok=True)

    # PDFファイル名（拡張子なし）
    pdf_name = os.path.splitext(os.path.basename(pdf_file))[0]

    # PDFファイルを開く
    doc = fitz.open(pdf_file)

    # 各ページをJPEGとして保存
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        output_path = os.path.join(output_folder, f'{pdf_name}_page_{page_num + 1:03}.jpg')
        pix.save(output_path)

    print(f'Converted {pdf_file} to JPEG files.')

if __name__ == "__main__":
    # 特定のPDFファイルのパス
    pdf_file = r"./pdf/Press.pdf"  # ここにPDFファイルのパスを指定

    # JPEGファイルを保存するフォルダのパス
    output_folder = r"./ConvertedImages"  # ここに出力フォルダのパスを指定

    # PDFをJPEGに変換
    convert_pdf_to_jpg(pdf_file, output_folder)