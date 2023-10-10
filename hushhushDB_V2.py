import sqlite3


def import_data(df):
    # Function to import data into candidates_table
    conn = sqlite3.connect('final_names.db')
    # Pushing the data from a data frame to the table
    df.to_sql('candidates_table', conn, if_exists='replace', index=False)
    conn.close()


def pass_query(query):
    # This is a helper function used to perform any query on the db(testing)
    # Connect to the SQLite database
    conn = sqlite3.connect('final_names.db')
    cursor = conn.cursor()
    # Query execution
    rows = cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows


def create_answers_table():
    try:
        conn = sqlite3.connect('final_names.db')
        cursor = conn.cursor()
        # Define the SQL statement to create the table
        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS answers_table (
            candidate_name TEXT,
            candidate_email TEXT,
            question_one_code TEXT,
            question_two_code TEXT,
            question_three_code TEXT
        );
        '''
        # Execute the SQL statement to create the table
        cursor.execute(create_table_sql)
        conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()


def insert_answers_db(candidate_name, candidate_email, question_one_code, question_two_code, question_three_code):
    # This function inserts candidate's coding answers to the db
    insert_sql = '''
    INSERT INTO answers_table (candidate_name, candidate_email, question_one_code, question_two_code, question_three_code)
    VALUES (?, ?, ?, ?, ?);
    '''
    values = (candidate_name, candidate_email, question_one_code, question_two_code, question_three_code)
    conn = sqlite3.connect('final_names.db')
    cursor = conn.cursor()
    # Insert statement execution
    cursor.execute(insert_sql, values)
    conn.commit()
    conn.close()




def email_check(email_to_check):
    # This function checks if the passed email_id is present in the database. This Fn is then used to restrict users from doing multiple answer submissions.
    conn = sqlite3.connect('final_names.db')
    cursor = conn.cursor()
    # Query execution
    query = '''
            SELECT candidate_email FROM answers_table WHERE candidate_email = ?
            '''
    cursor.execute(query, (email_to_check,))
    row = cursor.fetchone()
    conn.close()
    # Returns true, if the email is present
    return row is not None