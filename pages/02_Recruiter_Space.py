import yaml
from ui_fn import ui
import streamlit as st
from pathlib import Path
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from hushhushDB_V2 import pass_query
import pandas as pd

credentials_file_path = Path(__file__).parent.parent/"user_credentials/credentials.yaml"

if "name" in st.session_state and st.session_state["name"] == 'Candidate':
   st.caption("You have logged in as a Candidate. Logout from the candidate space and login as recruiter to access this content.")

else:
  with open(credentials_file_path) as file:
      user_config = yaml.load(file, Loader=SafeLoader)
      authenticator = stauth.Authenticate(user_config["credentials"],user_config["cookie"]["name"],user_config["cookie"]["key"],user_config["cookie"]["expiry_days"])

      name, authentication_status, username = authenticator.login("Login to Recruiter Space 🤵🏻", "main")

      if authentication_status == False:
        st.error("Username or Password is incorrect!")

      if authentication_status == None:
        st.warning("Please enter your username and password")

      if authentication_status:
        st.caption(f"Welcome, {name}! You are authenticated.")
        choice = st.sidebar.selectbox(label="Choose an activity", options=('Recruit','Candidate Submissions'))
        if choice == 'Recruit':
          ui()
        if choice == 'Candidate Submissions':
          candidate_submissions = pass_query('SELECT * FROM answers_table')
          if candidate_submissions:
            st.subheader("Candidate Submissions:")
            df = pd.DataFrame(candidate_submissions, columns=["Candidate Name", "Candidate Email", "Code Q1", "Code Q2", "Code Q3"])
            st.dataframe(df, use_container_width=True)
          else:
            st.write("No Candidate Submissions received so far.")
        authenticator.logout("Logout", "main")

