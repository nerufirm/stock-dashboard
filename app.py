"""日本株ダッシュボード メインアプリケーション.

Streamlit + yfinance を使用した日本株分析ダッシュボード。
株価チャート、銘柄比較、財務指標の3つのタブで構成。
"""

import streamlit as st

from components.chart import render_chart
from components.comparison import render_comparison
from components.external_links import render_external_links
from components.financials import render_financials
from components.sidebar import render_sidebar
from utils.data import get_multiple_stocks, get_raw_ticker_info, get_stock_data, get_stock_info
from utils.favorites import init_favorites

st.set_page_config(
    page_title="日本株ダッシュボード",
    page_icon="📈",
    layout="wide",
)

init_favorites()

sidebar_result = render_sidebar()
selected_codes: list[str] = sidebar_result["selected_codes"]
period: str = sidebar_result["period"]
chart_type: str = sidebar_result["chart_type"]

st.title("日本株ダッシュボード")

if not selected_codes:
    st.info("サイドバーから銘柄を選択してください")
else:
    tab_chart, tab_compare, tab_financials, tab_links = st.tabs(
        ["📈 株価チャート", "📊 銘柄比較", "📋 財務指標", "🔗 外部情報"]
    )

    primary_code = selected_codes[0]

    with tab_chart:
        with st.spinner("株価データを取得中..."):
            df = get_stock_data(primary_code, period)

        if df is not None:
            stock_info = get_stock_info(primary_code)
            stock_name = (
                stock_info.get("name", primary_code)
                if stock_info is not None
                else primary_code
            )
            st.subheader(f"{stock_name}（{primary_code}）")

            chart_type_label = "ローソク足" if chart_type == "candlestick" else "ライン"
            render_chart(df, primary_code, chart_type_label)
        else:
            st.error(f"銘柄 {primary_code} のデータを取得できませんでした")

    with tab_compare:
        if len(selected_codes) < 2:
            st.warning("2つ以上の銘柄を選択してください")
        else:
            with st.spinner("比較データを取得中..."):
                stocks_data = get_multiple_stocks(selected_codes, period)

            if stocks_data:
                render_comparison(stocks_data, "price")
            else:
                st.error("比較データの取得に失敗しました")

    with tab_financials:
        with st.spinner("財務情報を取得中..."):
            raw_info = get_raw_ticker_info(primary_code)

        if raw_info is not None:
            stock_name = (
                raw_info.get("longName")
                or raw_info.get("shortName", primary_code)
            )
            st.subheader(f"{stock_name}（{primary_code}）の財務指標")
            render_financials(raw_info)
        else:
            st.error(f"銘柄 {primary_code} の財務情報を取得できませんでした")

    with tab_links:
        render_external_links(primary_code)
