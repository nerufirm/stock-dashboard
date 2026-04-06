"""yfinanceから日本株データを取得するユーティリティモジュール."""

import logging

import pandas as pd
import yfinance as yf

logger = logging.getLogger(__name__)

_TOKYO_SUFFIX = ".T"


def _to_ticker_symbol(code: str) -> str:
    """銘柄コードに東証サフィックスを付与する."""
    code = code.strip()
    if not code.endswith(_TOKYO_SUFFIX):
        return f"{code}{_TOKYO_SUFFIX}"
    return code


def validate_stock_code(code: str) -> bool:
    """銘柄コードが有効かチェックする.

    東証の銘柄コード形式（4桁の数字）を検証し、
    yfinanceでデータが取得可能かも確認する。

    Args:
        code: 銘柄コード（例: "7203"）

    Returns:
        有効な銘柄コードの場合True
    """
    code = code.strip()
    if not code.isdigit() or len(code) != 4:
        return False

    try:
        ticker = yf.Ticker(_to_ticker_symbol(code))
        info = ticker.info
        return info is not None and info.get("regularMarketPrice") is not None
    except Exception:
        logger.warning("銘柄コード %s の検証に失敗しました", code)
        return False


def get_stock_data(code: str, period: str = "1y") -> pd.DataFrame | None:
    """指定銘柄のOHLCVデータを取得する.

    Args:
        code: 銘柄コード（例: "7203"）
        period: 取得期間（"1mo", "3mo", "6mo", "1y", "3y"）

    Returns:
        OHLCVデータのDataFrame。取得失敗時はNone。
    """
    try:
        symbol = _to_ticker_symbol(code)
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)

        if df.empty:
            logger.warning("銘柄 %s のデータが空です（period=%s）", code, period)
            return None

        return df
    except Exception:
        logger.warning("銘柄 %s のデータ取得に失敗しました", code)
        return None


def get_stock_info(code: str) -> dict | None:
    """銘柄の企業情報を取得する.

    Args:
        code: 銘柄コード（例: "7203"）

    Returns:
        企業情報の辞書。取得失敗時はNone。
        含まれるキー:
            name, marketCap, per, pbr, dividendYield,
            roe, roa, eps, revenue, operatingMargin
    """
    try:
        symbol = _to_ticker_symbol(code)
        ticker = yf.Ticker(symbol)
        info = ticker.info

        if info is None:
            return None

        return {
            "name": info.get("longName") or info.get("shortName", "不明"),
            "marketCap": info.get("marketCap"),
            "per": info.get("trailingPE") or info.get("forwardPE"),
            "pbr": info.get("priceToBook"),
            "dividendYield": info.get("dividendYield"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "eps": info.get("trailingEps") or info.get("forwardEps"),
            "revenue": info.get("totalRevenue"),
            "operatingMargin": info.get("operatingMargins"),
        }
    except Exception:
        logger.warning("銘柄 %s の企業情報取得に失敗しました", code)
        return None


def get_raw_ticker_info(code: str) -> dict | None:
    """銘柄のyfinance生データ（ticker.info）を取得する.

    Args:
        code: 銘柄コード（例: "7203"）

    Returns:
        yfinanceのticker.info辞書そのまま。取得失敗時はNone。
    """
    try:
        symbol = _to_ticker_symbol(code)
        ticker = yf.Ticker(symbol)
        info = ticker.info

        if info is None:
            return None

        return dict(info)
    except Exception:
        logger.warning("銘柄 %s のticker.info取得に失敗しました", code)
        return None


def get_stock_name(code: str) -> str:
    """銘柄コードから銘柄名を取得する.

    Args:
        code: 銘柄コード（例: "7203"）

    Returns:
        銘柄名。取得失敗時は銘柄コードをそのまま返す。
    """
    try:
        symbol = _to_ticker_symbol(code)
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if info is not None:
            return info.get("longName") or info.get("shortName", code)
    except Exception:
        logger.warning("銘柄 %s の名前取得に失敗しました", code)
    return code


def get_multiple_stocks(
    codes: list[str], period: str = "1y"
) -> dict[str, pd.DataFrame]:
    """複数銘柄のOHLCVデータを一括取得する.

    Args:
        codes: 銘柄コードのリスト（例: ["7203", "6758"]）
        period: 取得期間（"1mo", "3mo", "6mo", "1y", "3y"）

    Returns:
        銘柄コードをキー、DataFrameを値とする辞書。
        取得失敗した銘柄は含まれない。
    """
    results: dict[str, pd.DataFrame] = {}

    for code in codes:
        df = get_stock_data(code, period)
        if df is not None:
            results[code] = df

    return results
