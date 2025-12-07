import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import datetime
import os
import streamlit as st

# Get database URL from environment variable (set in Streamlit secrets)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Creates and returns a PostgreSQL database connection."""
    if not DATABASE_URL:
        st.error("DATABASE_URL environment variable not set. Check your .env file or Streamlit secrets.")
        st.stop()
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        st.error(f"Database connection failed: {e}")
        st.stop()

def init_db():
    """Initializes the PostgreSQL database and creates the table if it doesn't exist."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id SERIAL PRIMARY KEY,
            rating INTEGER,
            review TEXT,
            response TEXT,
            summary TEXT,
            recommendations TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_submission(rating, review, response, summary, recommendations):
    """Saves a new submission to the database."""
    conn = get_db_connection()
    c = conn.cursor()
    created_at = datetime.now()
    c.execute('''
        INSERT INTO submissions (rating, review, response, summary, recommendations, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (rating, review, response, summary, recommendations, created_at))
    conn.commit()
    conn.close()

def fetch_all_submissions():
    """Fetches all submissions from the database."""
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM submissions ORDER BY created_at DESC", conn)
    conn.close()
    return df
