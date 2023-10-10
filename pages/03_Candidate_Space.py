import time
import yaml
import streamlit as st
from pathlib import Path
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from hushhushDB_V2 import insert_answers_db, email_check

credentials_file_path = Path(__file__).parent.parent/"user_credentials/candidate_login.yaml"

if "name" in st.session_state and st.session_state["username"] != '' and st.session_state["name"] != 'Candidate':
   st.caption("You have logged in as a Recruiter. Logout from the Recruiter Space and login as Candidate to access this content.")

else:
    with open(credentials_file_path) as file:
        user_config = yaml.load(file, Loader=SafeLoader)
        authenticator = stauth.Authenticate(user_config["credentials"],user_config["cookie"]["name"],user_config["cookie"]["key"],user_config["cookie"]["expiry_days"])

        name, authentication_status, username = authenticator.login("Login to Candidate Space 👨🏻‍🎓", "main")

        if authentication_status == False:
            st.error("Username or Password is incorrect!")

        if authentication_status == None:
            st.warning("Please enter your username and password")

        if authentication_status:
            st.caption(f"Welcome, {name}! Here is an online test for you. Best of luck!")

            with st.form(key="candidate_submission"):
                col1, col2 = st.columns(spec=2, gap="small")
                
                with col1:
                    candidate_name = st.text_input(label="Your Name")

                with col2:
                    candidate_email = st.text_input(label="Your Email", placeholder="johndoe@gmail.com")

                st.divider()
                st.title("Programming Questions:")

                st.subheader("Question 1:")

                st.markdown("*Design a class to efficiently find the Kth largest element in a stream of numbers. The class should have the following two things:*")
                st.markdown("**1.The constructor of the class should accept an integer array containing initial numbers from the stream and an integer ‘K’.**")
                st.markdown("**2.The class should expose a function add(int num) which will store the given number and return the Kth largest number.**")

                question_one_code = st.text_area(label="Your code:", key="question_one_code")

                st.subheader("Question 2:")

                st.markdown("*Given a sorted number array and two integers ‘K’ and ‘X’, find ‘K’ closest numbers to ‘X’ in the array. Return the numbers in the sorted order. ‘X’ is not necessarily present in the array.*")

                question_two_code = st.text_area(label="Your code:", key="question_two_code")

                st.subheader("Question 3:")

                st.markdown("*Given the root node of a binary tree, swap the ‘left’ and ‘right’ children for each node.*")

                question_three_code = st.text_area(label="Your code", key="question_three_code")

                submitted = st.form_submit_button("Submit Answers")

                if submitted:
                    if candidate_email == "" or candidate_name == "":
                        st.error("Candidate Email or Name left empty.")
                    else:
                        if not email_check(candidate_email):
                            insert_answers_db(candidate_name, candidate_email, question_one_code, question_two_code, question_three_code)
                            st.success("Your answers have been submitted.")
                        else:
                            st.warning("You have already submitted your answers", icon="⚠️")
            authenticator.logout("Logout", "main")