import streamlit as st
import psycopg2
import os

# Database se connect karne ki settings (Humne Compose se uthayi hain)
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = "db" # Service ka naam jo humne Compose mein rakha hai

st.title("Data Entry to Postgres")

name = st.text_input("Enter your Name:")
age = st.number_input("Enter your age:", min_value=1)

if st.button("Save to Database"):
    try:
        # Database connection logic
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()
        
        # Table banana (agar nahi hai toh)
        cur.execute("CREATE TABLE IF NOT EXISTS users (name TEXT, age INT);")
        
        # Data insert karna
        cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", (name, age))
        
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"Congratulations!! {name} has been saved successfully.")
    except Exception as e:
        st.error(f"Error: {e}")