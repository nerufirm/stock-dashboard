"""銘柄比較モジュール"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

COLORS = [
    "#4A90E2",
    "#F39C12",
    "#E74C3C",
    "#2ECC71",
    "#9B59B6",
    "#1ABC9C",
    "#E67E22",
    "#3498DB",
]


def render_comparison(stocks_data: dict[str, pd.DataFrame], mode: str) -> None:
    """銘柄比較チャートを描画する

    Args:
        stocks_data: {銘柄コード: DataFrame} の辞書
        mode: "price"（価格ベース） or "percent"（変化率ベース）
    """
    selected_mode = st.radio(
        "比較モード",
        options=["price", "percent"],
        format_func=lambda x: "価格ベース" if x == "price" else "変化率ベース",
        index=0 if mode == "price" else 1,
        horizontal=True,
        key="comparison_mode",
    )

    fig = go.Figure()

    for i, (code, df) in enumerate(stocks_data.items()):
        color = COLORS[i % len(COLORS)]

        if selected_mode == "price":
            y_values = df["Close"]
            y_label = "株価（円）"
        else:
            first_close = df["Close"].iloc[0]
            y_values = (df["Close"] / first_close) * 100 - 100
            y_label = "変化率（%）"

        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=y_values,
                mode="lines",
                name=code,
                line={"color": color, "width": 2},
            )
        )

    title = "銘柄比較（価格）" if selected_mode == "price" else "銘柄比較（変化率）"

    fig.update_layout(
        title=title,
        yaxis_title=y_label,
        height=500,
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E",
        font={"color": "#F5F5F5", "family": "Noto Sans JP, sans-serif"},
        legend={
            "bgcolor": "rgba(30, 30, 30, 0.8)",
            "font": {"color": "#F5F5F5"},
        },
        margin={"l": 50, "r": 20, "t": 50, "b": 20},
    )

    fig.update_xaxes(gridcolor="#333333")
    fig.update_yaxes(gridcolor="#333333")

    st.plotly_chart(fig, use_container_width=True)
