import streamlit as st
from sqlalchemy import inspect
import yaml
import streamlit as st

st.set_page_config(layout="centered", page_title="Filter", page_icon="📐")
st.markdown("""
    <style>
    div[data-testid='stSidebarNav'] ul {max-height:none}</style>
    """, unsafe_allow_html=True)

try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        if 'filter' not in config.keys():
            config['filter'] = {}
except Exception as e:
    config = {'filter': {}}

if 'connection' in st.session_state:
    st.sidebar.caption(f"🔗 {st.session_state.db_name.capitalize()}")

    st.subheader('Filter table')
    table_filter = st.selectbox('Table filter', ['include', 'exclude'],
                                index=0 if config.get('filter').get('table_filter', 'include') == 'include' else 1)
    tables = st.text_area('Tables (one per line)', value="\n".join(config.get('filter').get('tables', ''))).split('\n')

    st.subheader('Filter fields')
    field_filter = st.selectbox('Field filter', ['include', 'exclude'],
                                index=0 if config.get('filter').get('field_filter', 'include') == 'include' else 1)
    fields = st.text_area('Fields (one per line)', value="\n".join(config.get('filter').get('fields', ''))).split('\n')

    if st.button("Save"):
        config['filter'] = {'table_filter': table_filter, 'field_filter': field_filter, 'tables': tables, 'fields': fields}

        with open('config.yaml', 'w') as file:
            yaml.safe_dump(config, file)




else:
    st.error("There is no database connection!")