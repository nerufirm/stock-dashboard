"""株価チャート描画モジュール"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


def render_chart(df: pd.DataFrame, code: str, chart_type: str) -> None:
    """メインのチャート描画関数

    Args:
        df: 株価データ（Open, High, Low, Close, Volume カラムを含む）
        code: 銘柄コード
        chart_type: "ローソク足" または "ライン"
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
        subplot_titles=(f"{code} 株価", "出来高"),
    )

    if chart_type == "ローソク足":
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                increasing_line_color="#E74C3C",
                increasing_fillcolor="#E74C3C",
                decreasing_line_color="#3498DB",
                decreasing_fillcolor="#3498DB",
                name="株価",
            ),
            row=1,
            col=1,
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                mode="lines",
                line={"color": "#4A90E2", "width": 2},
                name="終値",
            ),
            row=1,
            col=1,
        )

    fig.add_trace(
        go.Bar(
            x=df.index,
            y=df["Volume"],
            marker_color="#4A90E2",
            opacity=0.6,
            name="出来高",
        ),
        row=2,
        col=1,
    )

    fig.update_layout(
        height=500,
        template="plotly_dark",
        paper_bgcolor="#1E1E1E",
        plot_bgcolor="#1E1E1E",
        font={"color": "#F5F5F5", "family": "Noto Sans JP, sans-serif"},
        xaxis_rangeslider_visible=False,
        showlegend=False,
        margin={"l": 50, "r": 20, "t": 40, "b": 20},
    )

    fig.update_xaxes(gridcolor="#333333")
    fig.update_yaxes(gridcolor="#333333")

    st.plotly_chart(fig, use_container_width=True)
