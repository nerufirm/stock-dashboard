"""サイドバーUIモジュール.

銘柄コード入力、お気に入り管理、期間・チャート種類の選択を提供する。
"""

import streamlit as st

from utils.data import validate_stock_code
from utils.favorites import add_favorite, get_favorites, init_favorites, remove_favorite

_NOTO_SANS_JP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');

[data-testid="stSidebar"], [data-testid="stSidebar"] * {
    font-family: 'Noto Sans JP', sans-serif !important;
}
</style>
"""

_PERIOD_OPTIONS: dict[str, str] = {
    "1ヶ月": "1mo",
    "3ヶ月": "3mo",
    "6ヶ月": "6mo",
    "1年": "1y",
    "3年": "3y",
}

_CHART_TYPE_OPTIONS: dict[str, str] = {
    "ローソク足": "candlestick",
    "ライン": "line",
}


def render_sidebar() -> dict:
    """サイドバー全体を描画し、ユーザーの選択結果を返す.

    Returns:
        dict: ユーザーの選択結果
            - selected_codes (list[str]): 選択された銘柄コードのリスト
            - period (str): yfinanceのperiodパラメータ
            - chart_type (str): チャート種類（"candlestick" or "line"）
    """
    init_favorites()

    with st.sidebar:
        st.markdown(_NOTO_SANS_JP_CSS, unsafe_allow_html=True)
        st.header("日本株ダッシュボード")

        # --- 銘柄コード入力 ---
        st.subheader("銘柄を追加")
        input_code = st.text_input(
            "銘柄コード（4桁）",
            placeholder="例: 7203",
            max_chars=4,
            key="stock_code_input",
        )

        if st.button("お気に入りに追加", key="add_favorite_btn"):
            if input_code:
                if validate_stock_code(input_code):
                    add_favorite(input_code)
                    st.success(f"{input_code} を追加しました")
                else:
                    st.error("無効な銘柄コードです。4桁の数字を入力してください。")
            else:
                st.warning("銘柄コードを入力してください。")

        st.divider()

        # --- お気に入り銘柄リスト ---
        st.subheader("お気に入り銘柄")
        favorites = get_favorites()

        if not favorites:
            st.info("お気に入り銘柄がありません。上から追加してください。")
        else:
            selected_codes = []
            for code in favorites:
                col_check, col_del = st.columns([3, 1])
                with col_check:
                    is_selected = st.checkbox(
                        code,
                        value=True,
                        key=f"fav_check_{code}",
                    )
                    if is_selected:
                        selected_codes.append(code)
                with col_del:
                    if st.button(
                        "削除",
                        key=f"fav_del_{code}",
                    ):
                        remove_favorite(code)
                        st.rerun()

        st.divider()

        # --- 期間選択 ---
        st.subheader("表示期間")
        period_label = st.radio(
            "期間を選択",
            options=list(_PERIOD_OPTIONS.keys()),
            index=3,  # デフォルト: 1年
            key="period_radio",
            label_visibility="collapsed",
        )
        period = _PERIOD_OPTIONS[period_label]

        st.divider()

        # --- チャート種類切替 ---
        st.subheader("チャート種類")
        chart_type_label = st.radio(
            "チャート種類を選択",
            options=list(_CHART_TYPE_OPTIONS.keys()),
            index=0,  # デフォルト: ローソク足
            key="chart_type_radio",
            label_visibility="collapsed",
        )
        chart_type = _CHART_TYPE_OPTIONS[chart_type_label]

    return {
        "selected_codes": selected_codes if favorites else [],
        "period": period,
        "chart_type": chart_type,
    }
