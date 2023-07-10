
import streamlit as st
import yaml
from sqlalchemy import create_engine

try:
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
        if 'connection' not in config.keys():
            config['connection'] = {}
except Exception as e:
    config = {'connection':{}}

st.set_page_config(page_title="SQL Config", page_icon="🔗")
st.markdown("""
    <style>
    div[data-testid='stSidebarNav'] ul {max-height:none}</style>
    """, unsafe_allow_html=True)

st.subheader('Enter the SQL connection parameters:')
user = st.text_input('Username', value=config.get('connection').get('username', ''))
password = st.text_input('Password', type='password', value=config.get('connection').get('password', ''))
host = st.text_input('Host', value=config.get('connection').get('host', ''))
port = st.text_input('Port', value=config.get('connection').get('port', ''))
database = st.text_input('Database', value=config.get('connection').get('database', ''))

if st.button('🔗 Connect to database'):
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
    try:
        config['connection'] = {'username': user, 'password': password, 'host': host, 'port': port, 'database': database}

        with open('config.yaml', 'w') as file:
            yaml.safe_dump(config, file)

        connection = engine.connect()

        st.session_state["connection"] = connection
        st.session_state.db_name = database
    except Exception as e:
        st.error(f'Failed to connect: {e}')

if 'connection' in st.session_state:
    st.sidebar.caption(f"🔗 {st.session_state.db_name.capitalize()}")
    st.success('Successfully connected!')