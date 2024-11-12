import streamlit as st
from src.PDFtoImages import convert_pdf_to_jpg
from src.GetPageNo import GetPageNo
from src.RagClass import Rag
from src.ChromaSearcher import MarkdownSearcher
import os
import shutil
def main():
    st.title("PDF検索アプリケーション")
    # サイドバーでPDFファイルを選択
    st.sidebar.header("PDFファイルを選択")
    pdf_options = {
        "BSA071000 法定定期自主検査実施要領": "data/BSA071000 法定定期自主検査実施要領.pdf",
        "BSA120200 動力プレス機械安全基準：通則": "data/BSA120200 動力プレス機械安全基準：通則.pdf"
    }
    selected_pdf = st.sidebar.selectbox(
        "PDFを選択してください",
        options=list(pdf_options.keys())
    )
    pdf_path = pdf_options[selected_pdf]
    # 検索クエリの入力
    query = st.text_input("検索したい内容を入力してください")
    if st.button("検索"):
        if query:
            with st.spinner("検索中..."):
                try:
                    # ConvertedImagesディレクトリのクリーンアップ
                    output_folder = "./ConvertedImages"
                    if os.path.exists(output_folder):
                        shutil.rmtree(output_folder)
                    os.makedirs(output_folder)
                    # PDFの名前を抽出
                    pdf_name = selected_pdf
                    # 検索の実行
                    searcher = MarkdownSearcher()
                    file_name = searcher.get_markdown_file_name(pdf_name)
                    st.info(f"検索対象ファイル: {file_name}")
                    # 検索実行
                    results = searcher.search(
                        file_name,
                        query,
                        n_results=3,
                        alpha=0.1
                    )
                    if results:
                        # 検索結果の表示
                        st.subheader("検索結果")
                        for i, result in enumerate(results, 1):
                            with st.expander(f"結果 {i}"):
                                st.write(result['content'])
                                st.write(f"総合スコア: {result['score']:.3f}")
                                st.write(f"キーワードスコア: {result['keyword_score']:.3f}")
                                st.write(f"セマンティックスコア: {result['semantic_score']:.3f}")
                        # ページ番号の取得
                        page_numbers = GetPageNo(file_name, results[0]['content'])
                        st.info(f"該当ページ: {page_numbers}")
                        # PDFから画像を生成
                        convert_pdf_to_jpg(pdf_path, output_folder)
                        # RAG検索の実行
                        rag = Rag()
                        response = rag.process(file_name, output_folder, page_numbers, query)
                        # RAG検索結果の表示
                        st.subheader("詳細な回答")
                        st.write(response)
                    else:
                        st.warning("検索結果が見つかりませんでした。")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("検索クエリを入力してください。")
if __name__ == "__main__":
    main()