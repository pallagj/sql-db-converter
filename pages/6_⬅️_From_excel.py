import streamlit as st
from openpyxl import Workbook
from sqlalchemy import inspect
import yaml
import streamlit as st
import re
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows

st.set_page_config(layout="centered", page_title="From excel", page_icon="⬅️")
st.markdown("""
    <style>
    div[data-testid='stSidebarNav'] ul {max-height:none}</style>
    """, unsafe_allow_html=True)

try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
except Exception as e:
    config = {'transitions': {}}


def has_keys():
    return all(key in config for key in ['transitions', 'filter', 'connection'])


if 'connection' in st.session_state and has_keys():
    st.sidebar.caption(f"🔗 {st.session_state.db_name.capitalize()}")
    engine = st.session_state.connection.engine

    st.subheader("Convert from excel")

    table_filter = config.get('filter').get('table_filter')
    tables = config.get('filter').get('tables')

    field_filter = config.get('filter').get('field_filter')
    fields = config.get('filter').get('fields')

    transitions = config.get("transitions")

    # File upload
    file_name = st.text_input("Excel file name", "output.xlsx")

    if st.button('Upload Data'):
        try:
            df_uploaded = pd.read_excel(file_name, sheet_name=None)
            inserted_rows = 0
            inspector = inspect(engine)
            row_added = False

            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)

            table_names = inspector.get_table_names()
            tables_size = len(table_names)
            index = 0

            for table in table_names:
                if table in df_uploaded:
                    my_bar.progress(index / tables_size, text=progress_text)

                    # Get the columns for the table
                    df_table = df_uploaded[table]

                    # Remove the field types and max length info
                    df_table.columns = df_table.columns.str.replace(r' \(.+\)', '', regex=True)
                    df_table.columns = df_table.columns.str.replace(' ', '_')
                    df_table.columns = df_table.columns.str.upper()

                    # Get existing data from database
                    query = f'SELECT * FROM `{table}`'
                    df_existing = pd.read_sql(query, engine)

                    primary_key_columns = inspector.get_pk_constraint(table)['constrained_columns']

                    # Only keep rows in df_table which do not yet exist in df_existing based on primary key
                    df_to_upload = pd.concat([df_table, df_existing[primary_key_columns]]).drop_duplicates(
                        subset=primary_key_columns, keep=False)

                    df_to_upload.to_sql(table, con=engine, if_exists='append', index=False)

                    if len(df_to_upload) > 0:
                        st.success(f'Successfully uploaded {len(df_to_upload)} rows to {table} table!')
                        row_added = True

                index += 1
            if not row_added:
                st.success(f'No added row!')
        except Exception as e:
            st.error(f'Failed to upload data: {e}')
else:
    st.error("There is no database connection!")
