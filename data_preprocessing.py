import pandas as pd
import ast
import re
import nltk
from datetime import datetime, timezone
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import logging


# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Create a logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log', level=logging.ERROR)





# Custom decorator for error logging
def log_errors(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error in function {func.__name__}: {str(e)}")
            return None
    return wrapper

@log_errors
def preprocess_dataframe(input_df):
    try:
        df_main = input_df.copy()

        # Function to extract the most popular programming languages from repositories
        def extract_most_popular_languages(repo_list):
            most_popular_languages = []
            if pd.notnull(repo_list):
                repos = ast.literal_eval(repo_list)
                for repo in repos:
                    languages = repo.get("Languages", [])
                    if languages:
                        most_popular_languages.append(max(languages, key=languages.count))
                    else:
                        most_popular_languages.append(None)
            return most_popular_languages

        # Create new columns for the most popular programming languages
        for i in range(1, 4):  # Create columns proglang1, proglang2, ..., proglang5
            col_name = f"proglang{i}"
            df_main[col_name] = df_main["Top Repositories"].apply(extract_most_popular_languages).str[i - 1]

        # Fill NaN values in language columns
        column_names = ['proglang1', 'proglang2', 'proglang3']
        for c in column_names:
            df_main[c] = df_main[c].fillna("")

        #Dropping duplicates
        df_main = df_main.drop_duplicates(subset=['Username'])


        # Drop unused columns
        columns_to_drop = ['Name', 'Email', 'GitHub URL', 'Blog', 'Top Repositories']
        df_main = df_main.drop(columns_to_drop, axis=1)

        # Reset the index and remove 'Unnamed' columns
        df_main.reset_index(drop=True, inplace=True)
        df_main = df_main.loc[:, ~df_main.columns.str.contains('^Unnamed')]

        # Calculate GitHub experience in years
        df_main['Created At'] = pd.to_datetime(df_main['Created At'])
        current_datetime = datetime.now(timezone.utc)
        df_main['github_exp'] = ((current_datetime - df_main['Created At']).dt.days / 365.25).round(1)
        df_main = df_main.drop(['Created At'], axis=1)


        # List of columns to scale and inverse transform
        global scaler
        columns_to_scale = ['Followers', 'Following', 'Public Gists', 'Public Repos', 'github_exp']
        scaler = MinMaxScaler()
        scaler.fit(df_main[columns_to_scale])
        df_main[columns_to_scale] = scaler.transform(df_main[columns_to_scale])



        # Drop additional unused columns
        unused_columns = ['Company', 'Username', 'Location', 'Bio']
        df_main = df_main.drop(unused_columns, axis=1)

        # Perform one-hot encoding for 'domain' column
        one_hot_encoded = pd.get_dummies(df_main['domain'], prefix='domain')
        df_main = pd.concat([df_main, one_hot_encoded], axis=1)
        df_main = df_main.drop(['domain'], axis=1)

        # Function to preprocess text data
        def preprocess_text(text):
            text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
            text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove emojis and special characters
            text = re.sub(r'\s+', ' ', text)  # Remove additional spaces and digits
            text = text.lower()  # Convert to lowercase
            tokens = word_tokenize(text)  # Tokenize the text
            stop_words = set(stopwords.words('english'))
            filtered_tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
            return filtered_tokens

        column_name = ['proglang1', 'proglang2','proglang3',]
        for c in column_name:
            df_main[c] = df_main[c].apply(preprocess_text)
            df_main[c] = df_main[c].astype(str)

        # Cleaning the unique language and repo topic
        def clean_languages(languages):
            languages = languages.strip("[]").replace("'", "").split(", ")
            return ', '.join(languages)
        for c in column_name:
            df_main[c] = df_main[c].apply(clean_languages)

        # Replace 'c' with 'clang' since TF-IDF doesn't consider single letters
        old_value = 'c'
        new_value = 'clang'
        for c in column_name:
            df_main[c] = df_main[c].replace(old_value, new_value)

        # Conducting the TF-IDF
        programming_languages = df_main["proglang1"] + " " + df_main["proglang2"] + " " + df_main["proglang3"]  # Concatenate the columns
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(programming_languages)
        tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=tfidf_vectorizer.get_feature_names_out())
        df_main = pd.concat([df_main, tfidf_df], axis=1)

        # Drop the original programming language columns
        df_main.drop(columns=["proglang1", "proglang2","proglang3"], inplace=True)

        # # Save the preprocessed DataFrame
        # df_main.to_csv('Py_Files/preprocessed.csv', index=False)
        
        return df_main

    except Exception as e:
        # Handle exceptions gracefully and log the error
        print(f"An error occurred: {e}")
        return None

@log_errors
def filter_dataframe(input_df,user_exp,user_proglang):
    try:
        df_main = input_df.copy()
        columns_to_scale = ['Followers', 'Following', 'Public Gists', 'Public Repos', 'github_exp']
        df_main[columns_to_scale] = scaler.inverse_transform(df_main[columns_to_scale])


        temp_df=df_main.copy()
        #applying the user_exp filter
        df_main = df_main[df_main['github_exp'] >= user_exp]
        if df_main is not None:

            print("user experience filter applied successfully")
            language_to_check = user_proglang
            mask = df_main[language_to_check].any(axis=1)
            filtered_df = df_main[mask]

            if filtered_df is not None:
                df_main=filtered_df.copy()
                print("user prog language filter applied successfully")
            else:
                print("users with filtered prog language is not found, rolling back to default")
                df_main=temp_df.copy()

        else:
            print("users with filtered experience is not found, rolling back to default")
            df_main=temp_df.copy()

        return df_main


    except Exception as e:
    # Handle exceptions gracefully and log the error
        print(f"An error occurred: {e}")
        return None




if __name__ == "__main__":
    #Testing the function
    df_main = pd.read_csv('Datasets/github_final_dataset.csv')
    print(df_main)

