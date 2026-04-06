"""外部情報サイトリンクモジュール.

選択銘柄の外部サイト（Yahoo!ファイナンス、株探、みんかぶ、TDnet、EDINET）への
リンクを生成し、選択表示する。
"""

from datetime import date

import streamlit as st

_SITES: list[dict[str, str]] = [
    {
        "name": "Yahoo!ファイナンス",
        "category": "株価・ニュース",
        "description": "今日の株価・チャート・掲示板を確認",
        "url_template": "https://finance.yahoo.co.jp/quote/{code}.T",
        "icon": "🟣",
    },
    {
        "name": "株探（かぶたん）",
        "category": "株価・ニュース",
        "description": "今日の決算速報・銘柄ニュースを確認",
        "url_template": "https://kabutan.jp/stock/?code={code}",
        "icon": "🟢",
    },
    {
        "name": "みんかぶ",
        "category": "株価・ニュース",
        "description": "今日の予想・目標株価・口コミを確認",
        "url_template": "https://minkabu.jp/stock/{code}",
        "icon": "🔵",
    },
    {
        "name": "TDnet（東証開示システム）",
        "category": "決算・IR情報（一次情報）",
        "description": "今日の適時開示情報を検索",
        "url_template": (
            "https://www.release.tdnet.info/inbs/I_list_001_{today}.html"
        ),
        "icon": "🟠",
    },
    {
        "name": "EDINET",
        "category": "決算・IR情報（一次情報）",
        "description": "有価証券報告書など法定開示書類を検索",
        "url_template": "https://disclosure2.edinet-fsa.go.jp/WZEK0040.aspx",
        "icon": "🔴",
    },
]


def render_external_links(code: str) -> None:
    """選択銘柄の外部サイトリンクを表示する.

    Args:
        code: 銘柄コード（例: "7203"）
    """
    st.subheader(f"銘柄コード: {code} の外部情報サイト")

    selected_sites = st.multiselect(
        "表示するサイトを選択",
        options=[site["name"] for site in _SITES],
        default=[site["name"] for site in _SITES],
        key="external_sites_select",
    )

    if not selected_sites:
        st.info("表示するサイトを選択してください")
        return

    categories: dict[str, list[dict[str, str]]] = {}
    for site in _SITES:
        if site["name"] not in selected_sites:
            continue
        category = site["category"]
        if category not in categories:
            categories[category] = []
        categories[category] = [*categories[category], site]

    for category, sites in categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(len(sites))

        for col, site in zip(cols, sites):
            today_str = date.today().strftime("%Y%m%d")
            url = site["url_template"].format(code=code, today=today_str)
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #2D2D2D;
                        border-radius: 10px;
                        padding: 20px;
                        text-align: center;
                        border: 1px solid #444;
                    ">
                        <div style="font-size: 2em;">{site["icon"]}</div>
                        <h4 style="margin: 10px 0 5px 0;">{site["name"]}</h4>
                        <p style="color: #AAA; font-size: 0.85em;">{site["description"]}</p>
                        <a href="{url}" target="_blank" style="
                            display: inline-block;
                            background-color: #4A90E2;
                            color: white;
                            padding: 8px 20px;
                            border-radius: 5px;
                            text-decoration: none;
                            margin-top: 10px;
                        ">開く</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
