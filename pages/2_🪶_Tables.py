import math

import streamlit as st
from sqlalchemy import inspect
import pandas as pd

st.set_page_config(layout="wide", page_title="Tables", page_icon="🪶")
st.markdown("""
    <style>
    div[data-testid='stSidebarNav'] ul {max-height:none}</style>
    """, unsafe_allow_html=True)

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 1


if 'batch_size' not in st.session_state:
    st.session_state['batch_size'] = 25

if 'connection' in st.session_state:
    engine = st.session_state.connection.engine
    st.sidebar.caption(f"🔗 {st.session_state.db_name.capitalize()}")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    table = st.sidebar.selectbox('Selected table:', tables)

    if table:
        st.title(table)

        # Schema tab
        tabSchema, tabData = st.tabs(["Schema", "Data"])
        columns = inspector.get_columns(table)

        df = pd.DataFrame(columns)
        tabSchema.dataframe(df, use_container_width=True)

        # Data size
        querySize = f'SELECT COUNT(*) FROM `{table}`'
        dataSize = int(pd.read_sql_query(querySize, engine).values[0])

        # Data tab
        query = f"""
            SELECT *
                FROM `{table}`
                ORDER BY
                (   SELECT `COLUMN_NAME`
                    FROM `information_schema`.`COLUMNS`
                    WHERE (`TABLE_SCHEMA` = '{st.session_state.db_name}')
                      AND (`TABLE_NAME` = '{table}')
                      AND (`COLUMN_KEY` = 'PRI')
                )
                OFFSET {(st.session_state.current_page-1)*st.session_state.batch_size} ROWS FETCH NEXT {st.session_state.batch_size} ROWS ONLY
        """
        df = pd.read_sql_query(query, engine)
        tabData.dataframe(df, use_container_width=True)

        bottom_menu = tabData.columns((8, 1, 1))

        with bottom_menu[2]:
            batch_size = st.selectbox("Page Size", options=[25, 50, 100], key="batch_size")

        with bottom_menu[1]:
            total_pages = (int(math.ceil(dataSize / batch_size)))
            total_pages = total_pages if total_pages > 0 else 1
            current_page = st.number_input(
                "Page", min_value=1, max_value=total_pages, step=1, key="current_page"
            )

        with bottom_menu[0]:
            st.markdown(f"Page **{current_page}** of **{total_pages}** ")
else:
    st.error("There is no database connection!")
