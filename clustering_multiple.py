import pandas as pd
import numpy as np
import pickle
import logging
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# Create a logger
logger = logging.getLogger(__name__)
logging.basicConfig(filename='error.log', level=logging.ERROR)

secondary_cluster_word_map = {
    1: 'selected',
    0: 'rejected'
}

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
def cluster_data(input_df, model_pickle_path, input_domain):
    try:
        # Load your scaled DataFrame
        df_main = input_df.copy()
        # Load the model from the file
        with open(model_pickle_path, 'rb') as file:
            kmeans = pickle.load(file)
        #Conduct the prediction
        df_main['cluster'] = kmeans.fit_predict(df_main)
        # List of columns to check for '1'
        

        columns_to_map = ['domain_Artificial Intelligence', 'domain_automotive', 'domain_cybersecurity', 'domain_ecommerce', 'domain_entertainment and media', 'domain_healthcare','domain_industrial automation','domain_telecommunication']

        # Custom function to map column name to 'domain' if '1' is found
        def map_columns_to_domain(row):
            domain_columns = [col for col in columns_to_map if row[col] == 1]
            if domain_columns:
                return ' and '.join(domain_columns)
            else:
                return None


        # Apply the custom function to create the 'domain' column
        df_main['domain'] = df_main.apply(map_columns_to_domain, axis=1)
        # df_main.to_csv('Py_Files/trial.csv')


        # Separate data belonging to input domain
        df_main = df_main[df_main['domain'] == input_domain]
        # df_main.to_csv('Py_Files/trial.csv')
        df_main = df_main.drop(['cluster','domain'], axis=1)


        # Hyperparameter tuning for initialization settings
        init_methods = ['k-means++', 'random']
        random_seeds = [0, 42, 99]  # Different random seeds to try
        best_silhouette_score = -1  # Initialize with a negative value
        best_params = {}

        for init_method in init_methods:
            for random_seed in random_seeds:
                kmeans = KMeans(n_clusters=2, init=init_method, random_state=random_seed)
                kmeans.fit(df_main)
                silhouette_avg = silhouette_score(df_main, kmeans.labels_)

                if silhouette_avg > best_silhouette_score:
                    best_silhouette_score = silhouette_avg
                    best_params = {'init': init_method, 'random_seed': random_seed}

        print("Best initialization settings for secondary clustering:", best_params)
        print("Best Silhouette Score for secondary clustering:", best_silhouette_score)

        # Number of clusters
        n_clusters = 2
        # Initialize and fit KMeans model
        kmeans = KMeans(n_clusters=n_clusters, init=best_params['init'], random_state=best_params['random_seed'])
        df_main['cluster'] = kmeans.fit_predict(df_main)

        # Separate results belonging to 'selected' cluster
        df_main['cluster'] = df_main['cluster'].replace(secondary_cluster_word_map)
        df_main = df_main[df_main['cluster'] == 'selected']

        # df_main.to_csv("PY Files/result.csv", index=False)
        return df_main

    except Exception as e:
        logger.error(f"Error in cluster_data function: {str(e)}")
        return None


if __name__ == "__main__":
    pass
