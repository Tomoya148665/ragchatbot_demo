import streamlit as st
from src.PDFtoImages import convert_pdf_to_jpg
from src.GetPageNo import GetPageNo
from src.RagClass import Rag
from src.ChromaSearcher import MarkdownSearcher
import os
import shutil
from src.AllProcessor import allProcessor

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
                    allResult = allProcessor(pdf_path, query, ForUI=True)

                    if allResult["ChromaResult"]:
                        # 検索結果の表示
                        st.subheader("検索結果")
                        for i, result in enumerate(allResult["ChromaResult"], 1):
                            with st.expander(f"結果 {i}"):
                                st.write(result['content'])
                                st.write(f"総合スコア: {result['score']:.3f}")
                    else:
                        st.warning("該当するページが見つかりませんでした。")

                    if allResult["RAGResult"]:
                        st.subheader("詳細な回答")
                        st.write(allResult["RAGResult"]["response"])

                    else:
                        st.warning("検索結果が見つかりませんでした。")

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("検索クエリを入力してください。")

if __name__ == "__main__":
    main()