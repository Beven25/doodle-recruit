FROM python:3.8-slim

RUN pip install nltk

RUN pip install numpy

RUN pip install pandas

RUN pip install PyYAML

RUN pip install scikit-learn

RUN pip install streamlit

RUN pip install streamlit-authenticator

RUN mkdir doodle-project

WORKDIR /doodle-project

COPY Datasets/github_final_dataset.csv Datasets/github_final_dataset.csv
COPY K-means_model/kmeans_model_main.pkl K-means_model/kmeans_model_main.pkl

COPY pages/02_Recruiter_Space.py pages/02_Recruiter_Space.py
COPY pages/03_Candidate_Space.py pages/03_Candidate_Space.py
COPY pages/04_Register_Recruiter.py pages/04_Register_Recruiter.py

COPY user_credentials/candidate_login.yaml user_credentials/candidate_login.yaml
COPY user_credentials/credentials.yaml user_credentials/credentials.yaml

COPY cluster_and_push.py cluster_and_push.py
COPY clustering_multiple.py clustering_multiple.py
COPY data_preprocessing.py data_preprocessing.py

COPY final_names.db final_names.db
COPY hushhushDB_V1.py hushhushDB_V1.py
COPY hushhushDB_V2.py hushhushDB_V2.py

COPY output.csv output.csv

COPY send_email.py send_email.py

COPY ui_fn.py ui_fn.py

COPY streamlit_app.py streamlit_app.py

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py"]


