import sqlite3

def create_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('hushhushDB.db')
    cursor = conn.cursor()
    # Create a table with a schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates_table (
            id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            email TEXT,
            location TEXT,
            bio TEXT,
            company TEXT,
            github_url TEXT,
            blog TEXT,
            followers INTEGER,
            following INTEGER,
            public_gists INTEGER,
            created_on TEXT
            public_repos INTEGER,
            top_repos TEXT,
            domain TEXT,
        )
    ''')
    # Commit the table creation and close the connection
    conn.commit()
    conn.close()


def import_data(df):
    # Connect to the SQLite database
    conn = sqlite3.connect('final_names.db')
    # Pushing the data from a data frame to the table
    df.to_sql('candidates_table', conn, if_exists='replace', index=False)
    conn.close()


def pass_query(query):
    # Connect to the SQLite database
    conn = sqlite3.connect('final_names.db')
    cursor = conn.cursor()
    # Query execution
    rows = cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


