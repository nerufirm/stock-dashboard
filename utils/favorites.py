"""お気に入り銘柄の管理モジュール.

Streamlitのsession_stateを使用してお気に入り銘柄リストを管理する。
"""

import streamlit as st

_FAVORITES_KEY = "favorites"
_DEFAULT_FAVORITES = ["7203", "6758", "9984"]  # トヨタ、ソニー、ソフトバンクG


def init_favorites() -> None:
    """session_stateにお気に入りリストを初期化する.

    既にfavoritesキーが存在する場合は何もしない。
    デフォルトでトヨタ(7203)、ソニー(6758)、ソフトバンクG(9984)を設定。
    """
    if _FAVORITES_KEY not in st.session_state:
        st.session_state[_FAVORITES_KEY] = list(_DEFAULT_FAVORITES)


def add_favorite(code: str) -> None:
    """お気に入りに銘柄を追加する.

    Args:
        code: 銘柄コード（例: "7203"）

    既に追加済みの場合は何もしない。
    """
    init_favorites()
    code = code.strip()
    favorites = st.session_state[_FAVORITES_KEY]
    if code not in favorites:
        st.session_state[_FAVORITES_KEY] = [*favorites, code]


def remove_favorite(code: str) -> None:
    """お気に入りから銘柄を削除する.

    Args:
        code: 銘柄コード（例: "7203"）

    存在しない銘柄コードを指定した場合は何もしない。
    """
    init_favorites()
    code = code.strip()
    st.session_state[_FAVORITES_KEY] = [
        c for c in st.session_state[_FAVORITES_KEY] if c != code
    ]


def get_favorites() -> list[str]:
    """お気に入り銘柄コードのリストを取得する.

    Returns:
        お気に入り銘柄コードのリスト（コピー）
    """
    init_favorites()
    return list(st.session_state[_FAVORITES_KEY])
