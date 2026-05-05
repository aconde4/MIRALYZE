"""
Data upload view: file preview, validation, import and progress feedback.
"""

import os

import pandas as pd
import streamlit as st

from database.db_manager import clear_query_cache, execute_query
from etl.loader import load_file
from etl.transformer import transform_and_load
from etl.validator import validate
from metrics.calculator import calculate_metrics


def render():
    st.title("Cargar datos")

    uploaded_file = st.file_uploader(
        "Selecciona un archivo Excel",
        type=["xlsx", "xls"],
    )

    if uploaded_file is None:
        _show_import_history()
        return

    load_mode = st.radio(
        "Modo de carga",
        ["initial", "incremental"],
        format_func=lambda x: "Carga inicial" if x == "initial" else "Carga incremental",
        horizontal=True,
    )

    try:
        df_raw = load_file(uploaded_file, uploaded_file.name)
        uploaded_file.seek(0)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        return

    st.subheader("Vista previa del archivo")
    st.dataframe(df_raw.head(10), use_container_width=True, hide_index=True)
    st.caption(f"{len(df_raw)} filas leídas en total")

    if "validation_done" not in st.session_state:
        st.session_state.validation_done = False

    if st.button("Validar archivo", type="primary"):
        try:
            df_valid, df_rejected = validate(df_raw)
            st.session_state.df_valid = df_valid
            st.session_state.df_rejected = df_rejected
            st.session_state.validation_done = True
            st.session_state.total_rows = len(df_raw)
        except ValueError as e:
            st.error(f"Error de validación estructural: {e}")
            return

    if st.session_state.validation_done:
        df_valid = st.session_state.df_valid
        df_rejected = st.session_state.df_rejected
        total_rows = st.session_state.total_rows

        col1, col2, col3 = st.columns(3)
        col1.metric("Filas leídas", total_rows)
        col2.metric("Filas válidas", len(df_valid))
        col3.metric("Filas rechazadas", len(df_rejected))

        if not df_rejected.empty:
            st.warning(f"{len(df_rejected)} filas rechazadas")
            with st.expander("Ver motivos de rechazo"):
                cols_to_show = ["company_name", "year", "rejection_reason"]
                cols_available = [c for c in cols_to_show if c in df_rejected.columns]
                st.dataframe(
                    df_rejected[cols_available],
                    use_container_width=True,
                    hide_index=True,
                )

        if len(df_valid) > 0:
            if st.button("Importar datos validados", type="primary"):
                _run_import(
                    uploaded_file.name,
                    load_mode,
                    df_valid,
                    df_rejected,
                    total_rows,
                )
        else:
            st.warning("No hay filas válidas para importar.")

    st.markdown("---")
    _show_import_history()


def _run_import(file_name, load_mode, df_valid, df_rejected, total_rows):
    progress = st.progress(0, text="Preparando importación...")
    status = st.empty()

    def import_progress(current, total):
        pct = current / total if total else 1
        progress.progress(
            min(0.70, pct * 0.70),
            text=f"Importando filas validadas: {current}/{total}",
        )

    def metrics_progress(current, total):
        pct = current / total if total else 1
        progress.progress(
            0.70 + min(0.30, pct * 0.30),
            text=f"Recalculando métricas: {current}/{total}",
        )

    try:
        ext = os.path.splitext(file_name)[1].lower()
        status.info("Guardando empresas y datos financieros en Supabase...")
        result = transform_and_load(
            df_valid,
            df_rejected,
            file_name,
            ext,
            load_mode,
            total_rows,
            progress_callback=import_progress,
        )

        if result["affected_company_ids"]:
            status.info("Calculando métricas financieras...")
            calculate_metrics(
                result["affected_company_ids"],
                progress_callback=metrics_progress,
            )

        clear_query_cache()
        progress.progress(1.0, text="Importación completada")
        status.empty()
        st.success(
            f"Importación completada: {result['rows_accepted']} filas aceptadas, "
            f"{result['rows_rejected']} rechazadas."
        )

        st.session_state.validation_done = False
        for key in ("df_valid", "df_rejected"):
            if key in st.session_state:
                del st.session_state[key]

    except Exception as e:
        progress.empty()
        status.empty()
        st.error(f"Error durante la importación: {e}")


def _show_import_history():
    """Show the full import history."""
    with st.expander("Historial de importaciones"):
        imports = execute_query(
            """SELECT import_timestamp, file_name, file_type, load_mode,
                      rows_read, rows_accepted, rows_rejected, notes
               FROM import_log
               ORDER BY import_timestamp DESC"""
        )
        if imports:
            df = pd.DataFrame(imports)
            df.columns = [
                "Fecha", "Archivo", "Tipo", "Modo",
                "Leídas", "Aceptadas", "Rechazadas", "Notas",
            ]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No hay importaciones registradas.")
