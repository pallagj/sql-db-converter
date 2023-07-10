import streamlit as st

st.set_page_config(
    page_title="Excel and MariaDB migration",
    page_icon="🔗",
)

st.markdown("""
    <style>
    div[data-testid='stSidebarNav'] ul {max-height:none}</style>
    """, unsafe_allow_html=True)

st.write("# 🏃🏼‍♂️ Excel and MariaDB migration")

st.markdown(
"""
   The application provides the following main features 🚀:
    - 🔗 Connection configuration to a MariaDB database (host, port, user, password, etc.)
    - 🪧 Table and field filtering for export with support for regular expressions.
    - ✏️Customizable data type and property mappings from SQL to user-friendly names.
    - 🪶 Generation of Excel files from the database for data entry.
    - 👓 Import of new data entries from the Excel file back into the database.
"""
)

if 'connection' in st.session_state:
    st.sidebar.caption(f"🔗 {str(st.session_state.connection.engine.url).split('/')[3].capitalize()}")