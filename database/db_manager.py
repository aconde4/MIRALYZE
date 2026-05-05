"""
PostgreSQL/Supabase connection helpers.

The application uses SQL directly through psycopg. The database schema is
created once in Supabase using database/schema.sql; the app does not initialize
or migrate the database on startup.
"""

import os
import tomllib
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path


def _get_database_url() -> str:
    """Return the Supabase/Postgres connection URL from Streamlit secrets or env."""
    try:
        import streamlit as st

        url = st.secrets.get("SUPABASE_DB_URL")
        if url:
            return str(url)
    except Exception:
        pass

    url = os.getenv("SUPABASE_DB_URL")
    if url:
        return url

    secrets_path = Path.cwd() / ".streamlit" / "secrets.toml"
    if secrets_path.exists():
        with secrets_path.open("rb") as file:
            url = tomllib.load(file).get("SUPABASE_DB_URL")
        if url:
            return str(url)

    raise RuntimeError(
        "SUPABASE_DB_URL no está configurada. Añádela a st.secrets o al entorno."
    )


@contextmanager
def get_connection():
    """Open a PostgreSQL connection and commit/rollback automatically."""
    try:
        import psycopg
        from psycopg.rows import dict_row
    except ImportError as exc:
        raise RuntimeError(
            "Falta psycopg. Instala las dependencias con `pip install -r requirements.txt`."
        ) from exc

    conn = psycopg.connect(_get_database_url(), row_factory=dict_row)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Kept for compatibility. Supabase schema is applied manually."""
    return None


def execute_query(query: str, params: tuple = ()) -> list[dict]:
    """Run a SELECT query and return rows as dictionaries."""
    try:
        return _cached_execute_query(query, tuple(params or ()))
    except RuntimeError:
        return _execute_query_uncached(query, tuple(params or ()))


def _execute_query_uncached(query: str, params: tuple = ()) -> list[dict]:
    """Run a SELECT query without Streamlit caching."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return [_coerce_row(row) for row in cur.fetchall()]


try:
    import streamlit as st

    @st.cache_data(ttl=300, show_spinner=False)
    def _cached_execute_query(query: str, params: tuple = ()) -> list[dict]:
        return _execute_query_uncached(query, params)

except Exception:
    def _cached_execute_query(query: str, params: tuple = ()) -> list[dict]:
        raise RuntimeError("Streamlit cache unavailable")


def clear_query_cache() -> None:
    """Clear cached SELECT results after data-changing operations."""
    try:
        _cached_execute_query.clear()
    except Exception:
        pass


def execute_insert(query: str, params: tuple = ()):
    """Run an INSERT/UPSERT query and return the first RETURNING value if present."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if cur.description:
                row = cur.fetchone()
                if not row:
                    return None
                row = _coerce_row(row)
                clear_query_cache()
                return next(iter(row.values())) if isinstance(row, dict) else row[0]
            clear_query_cache()
            return None


def execute_update(query: str, params: tuple = ()) -> int:
    """Run an UPDATE/DELETE query and return the affected row count."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            clear_query_cache()
            return cur.rowcount


def execute_many(query: str, params_list: list[tuple]) -> None:
    """Run a statement for multiple parameter tuples."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.executemany(query, params_list)
            clear_query_cache()


def _coerce_row(row: dict) -> dict:
    return {
        key: float(value) if isinstance(value, Decimal) else value
        for key, value in dict(row).items()
    }
