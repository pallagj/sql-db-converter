import streamlit as st
from sqlalchemy import inspect
import yaml
import streamlit as st

st.set_page_config(layout="centered", page_title="Transitions", page_icon="📜")
st.markdown("""
    <style>
    div[data-testid='stSidebarNav'] ul {max-height:none}</style>
    """, unsafe_allow_html=True)
try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        if 'transitions' not in config.keys():
            config['transitions'] = {}

except Exception as e:
    config = {'transitions': {}}

if 'connection' in st.session_state:
    st.sidebar.caption(f"🔗 {st.session_state.db_name.capitalize()}")

    st.subheader("Transitions")

    mysql_types = config.get('transitions')

    # Táblázat létrehozása
    transitions = st.data_editor(mysql_types,  use_container_width=True, num_rows="dynamic")

    if st.button("Save"):
        config['transitions'] = transitions

        with open('config.yaml', 'w') as file:
            yaml.safe_dump(config, file)


else:
    st.error("There is no database connection!")