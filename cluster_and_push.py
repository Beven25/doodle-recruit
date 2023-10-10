import pandas as pd
from data_preprocessing import preprocess_dataframe
from clustering_multiple import cluster_data
from data_preprocessing import filter_dataframe
from hushhushDB_V1 import import_data
from datetime import datetime
import random
import streamlit as st

def calculate_coding_experience(df):
    """Calculate coding experience based on 'Created At' column."""
    df['Created At'] = pd.to_datetime(df['Created At'])
    current_date = pd.Timestamp(datetime.now().date())
    df['Created At'] = df['Created At'].dt.tz_localize(None)
    df['github_exp'] = round((current_date - df['Created At']).dt.days / 365.25, 1)
    return df

def map_input_to_domain(input_value, domain_match):
    """Map input domain to its standardized name."""
    return domain_match.get(input_value, "Unknown Domain")

@st.cache_data
def merge_and_filter(main_df, final_df, domain_filter):
    """Merge and filter DataFrames based on common columns."""
    if domain_filter:
        main_df = main_df[main_df['domain'] == domain_filter]
    merged_df = pd.merge(final_df, main_df, on=['Followers', 'Following', 'github_exp'], how='inner')
    output_df = merged_df[['Username', 'Followers', 'Public Gists_x', 'Public Repos_x', 'github_exp', 'domain', 'cluster', 'Email']]
    output_df = output_df[~output_df['Username'].duplicated()]
    return output_df

@st.cache_data
def cluster_push(user_exp, user_domain,prog_lang):
    input_csv_path = 'Datasets/github_final_dataset.csv'
    prim_model_path = 'K-means_model/kmeans_model_main.pkl'
    random_emails = [
        "aneeth.Manikantan@gmail.com",
        "srujanbpgowda333@gmail.com",
        "hande.sumeet38@gmail.com",
        "rozario.rio12@gmail.com"
    ]

    domain_match = {
        'domain_Artificial Intelligence': 'Artificial Intelligence',
        'domain_automotive': 'automotive',
        'domain_cybersecurity': 'cybersecurity',
        'domain_ecommerce': 'ecommerce',
        'domain_entertainment and media': 'entertainment and media',
        'domain_healthcare': 'healthcare',
        'domain_industrial automation': 'industrial automation',
        'domain_telecommunication': 'telecommunication'
    }

    try:
        preprocessed_df = preprocess_dataframe(pd.read_csv(input_csv_path))

        if preprocessed_df is not None:
            clustered_df = cluster_data(preprocessed_df, prim_model_path, user_domain)
            print("Preprocessed and clustered successfully")
        else:
            print("Error occurred during preprocessing. Check error.log for details.")

        final_df = filter_dataframe(clustered_df, user_exp, prog_lang)

        if final_df is not None:
            print("Profile filtered successfully")
        else:
            print("Error occurred during filtering. Check error.log for details.")

        main_df = pd.read_csv(input_csv_path)
        main_df = calculate_coding_experience(main_df)
        main_domain = map_input_to_domain(user_domain, domain_match)
        final_df = merge_and_filter(main_df, final_df, main_domain)

        final_df['Email'] = random.choices(random_emails, k=len(final_df))
        final_df.to_csv('output.csv')

        if import_data(final_df):
            print("Data successfully pushed to the database")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    user_domain = 'domain_ecommerce'
    user_exp = 5
    cluster_push(user_exp, user_domain)
