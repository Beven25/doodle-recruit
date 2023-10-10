import yaml
import streamlit as st
from pathlib import Path
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

credentials_file_path = Path(__file__).parent.parent/"user_credentials/credentials.yaml"

with open(credentials_file_path) as file:
    user_config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(user_config["credentials"],user_config["cookie"]["name"],user_config["cookie"]["key"],user_config["cookie"]["expiry_days"])
try:
    if authenticator.register_user('Register Recruiter 🗒️', 'main', preauthorization=False):
        with open(credentials_file_path, 'w') as file:
            yaml.dump(user_config, file, default_flow_style=False) 
        st.success('Recruiter registered successfully. Go to Recruiter Space to login.')
except Exception as e:
    st.error(e)