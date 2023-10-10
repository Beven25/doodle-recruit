import streamlit as st
import sqlite3
import pandas as pd
import send_email
from cluster_and_push import cluster_push


def clicked():
    st.session_state.clicked = True

def ui():
    # Create a connection to the SQLite database
    try:
        conn = sqlite3.connect('final_names.db')
    except sqlite3.Error as e:
        st.error(f"An error occurred while connecting to the database: {e}")
    else:
        c = conn.cursor()

        # Streamlit UI
        # st.title('Candidate Filter')

        st.sidebar.header('Filter Criteria')

        domain_options = ['domain_Artificial Intelligence', 'domain_automotive', 'domain_cybersecurity', 'domain_ecommerce', 'domain_entertainment and media', 'domain_healthcare','domain_industrial automation','domain_telecommunication']
        domain = st.sidebar.selectbox('Select Domain:', domain_options)
        domain=str(domain)

        programming_languages = ['python', 'clang', 'javascript','css','go','java','html','kotlin','lua','php','ruby','rust','shell','typescript','scala','vue']
        selected_programming_language = st.sidebar.multiselect('Select Programming languages:', programming_languages)
  

        github_experience = st.sidebar.text_input('Minimum GitHub Experience:', '0')
        github_experience=int(github_experience)

        if 'clicked' not in st.session_state:
            st.session_state.clicked = False

        # if st.sidebar.button('Filter Candidates')
        st.sidebar.button('Filter Candidates', on_click=clicked)
        if st.session_state.clicked:
            try:
                # Ensure that the input for GitHub Experience is an integer
                cluster_push(github_experience,domain,selected_programming_language)

                # SQL query to filter candidates based on the selected domain and minimum GitHub experience
                c.execute('''
                    SELECT Username, Email FROM candidates_table ''')


                # Retrieve and display filtered candidates in a DataFrame
                filtered_candidates = c.fetchall()

                if filtered_candidates:
                    st.subheader('Matching Candidates:')
                    df = pd.DataFrame(filtered_candidates, columns=['Username', 'Email'])
                    # st.write(df)
                    # print(df)
                    st.dataframe(df, use_container_width=True)

                    # "Send Email" button
                    if st.button("Send Email"):
                        st.info("Email sending process started...", icon="ℹ️")
                        send_email.send_email()
                        st.success("Emails sent")

                else:
                    st.write('No candidates match the selected criteria.')
            except ValueError:
                st.error('Please enter a valid integer for GitHub Experience.')
            except sqlite3.Error as e:
                st.error(f"An error occurred while querying the database: {e}")
            finally:
                # Close the database connection
                conn.close()
        else:
            st.subheader("Use the filter criteria in the sidebar to shortlist candidates.")
        
        
