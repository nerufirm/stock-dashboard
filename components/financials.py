"""財務指標表示モジュール（解説付き）.

yfinanceから取得した企業情報を、解説テキスト付きで表示する。
"""

import streamlit as st

_METRICS: list[dict[str, str]] = [
    {
        "label": "PER（株価収益率）",
        "key": "trailingPE",
        "format": "number",
        "description": (
            "株価が1株当たり利益の何倍かを示す。"
            "低いほど割安の可能性。一般的な目安は15倍前後。"
        ),
        "suffix": "倍",
    },
    {
        "label": "PBR（株価純資産倍率）",
        "key": "priceToBook",
        "format": "number",
        "description": (
            "株価が1株当たり純資産の何倍かを示す。"
            "1倍以下は解散価値を下回っていることを意味し、割安とされる。"
        ),
        "suffix": "倍",
    },
    {
        "label": "配当利回り",
        "key": "dividendYield",
        "format": "percent",
        "description": (
            "株価に対する年間配当金の割合。"
            "高いほどインカムゲインが大きい。日本株の平均は約2%前後。"
        ),
        "suffix": "",
    },
    {
        "label": "時価総額",
        "key": "marketCap",
        "format": "oku",
        "description": (
            "企業の株式市場での評価額。株価×発行済み株式数で算出。"
            "企業規模を示す最も基本的な指標。"
        ),
        "suffix": "",
    },
    {
        "label": "ROE（自己資本利益率）",
        "key": "returnOnEquity",
        "format": "percent",
        "description": (
            "自己資本に対してどれだけ利益を上げたかを示す。"
            "投資家が重視する指標で、8%以上が目安。"
        ),
        "suffix": "",
    },
    {
        "label": "ROA（総資産利益率）",
        "key": "returnOnAssets",
        "format": "percent",
        "description": (
            "総資産に対してどれだけ利益を上げたかを示す。"
            "資産を効率的に使えているかの指標。5%以上が優良とされる。"
        ),
        "suffix": "",
    },
    {
        "label": "EPS（1株当たり利益）",
        "key": "trailingEps",
        "format": "yen",
        "description": (
            "1株あたりの純利益。高いほど収益力が強い。"
            "前年比で増加していれば成長している証拠。"
        ),
        "suffix": "",
    },
    {
        "label": "売上高",
        "key": "totalRevenue",
        "format": "oku",
        "description": (
            "企業の事業活動による総収入。"
            "企業規模と成長性を測る基本指標。"
        ),
        "suffix": "",
    },
    {
        "label": "営業利益率",
        "key": "operatingMargins",
        "format": "percent",
        "description": (
            "売上高に対する営業利益の割合。"
            "本業での稼ぐ力を示す。10%以上あれば優良企業とされる。"
        ),
        "suffix": "",
    },
]

_OKU_UNIT = 100_000_000


def _format_value(value: float | int | None, fmt: str, suffix: str) -> str:
    """指標の値をフォーマットする.

    Args:
        value: 指標の生の値（Noneの場合は「-」を返す）
        fmt: フォーマット種別（"number", "percent", "oku", "yen"）
        suffix: 数値の後ろに付ける接尾辞（"倍"など）

    Returns:
        表示用の文字列
    """
    if value is None:
        return "-"

    if fmt == "percent":
        return f"{value * 100:.2f}%"
    if fmt == "oku":
        oku_value = value / _OKU_UNIT
        return f"{oku_value:.0f}億円"
    if fmt == "yen":
        return f"{value:.2f}円"
    return f"{value:.2f}{suffix}"


def render_financials(info: dict) -> None:
    """財務指標を解説付きで表示する.

    2列レイアウトで各指標をst.metricで表示し、
    st.expanderで解説テキストを提供する。

    Args:
        info: yfinanceのticker.infoから取得した辞書
    """
    col_left, col_right = st.columns(2)
    columns = [col_left, col_right]

    for i, metric in enumerate(_METRICS):
        target_col = columns[i % 2]
        raw_value = info.get(metric["key"])
        display_value = _format_value(raw_value, metric["format"], metric["suffix"])

        with target_col:
            st.metric(label=metric["label"], value=display_value)
            with st.expander("解説"):
                st.write(metric["description"])
