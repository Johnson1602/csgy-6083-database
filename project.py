import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

# get database configuration
@st.cache
def get_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}

# perform sql queries
@st.cache
def query_db(sql: str):
    # print(f'Running query_db(): {sql}')
 
    db_info = get_config()
    # Connect to an existing database
    conn = psycopg2.connect(**db_info)
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # Execute a command: this creates a new table
    # the result is stored in the cursor, function 'execute' returns null
    cur.execute(sql)
    # Obtain data
    data = cur.fetchall() # can use fetchone() or fetchmany(size) instead
    column_names = [desc[0] for desc in cur.description]
    # Make the changes to the database persistent
    conn.commit()
    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)
    return df

st.title("Mobile Device Database")

menu = ["Home","Login","Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

# Security
# passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# register new user
def register(username, password, age, gender, email):
    db_info = get_config()
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    add_user = f"insert into users (username, age, gender, password, email) values ('{username}', {age}, '{gender}', '{password}', '{email}');"
    cur.execute(add_user)
    conn.commit()
    cur.close()
    conn.close()

# User Login
def login(username, password):
    check = f"select * from users where username = '{username}' and password = '{password}';"
    return not query_db(check).empty

# Sidebar
if choice == "Home":
    st.subheader("Home")
    "Here are all the companies we have"
    query_all_companies = "select * from companies;"
    all_companies = query_db(query_all_companies)
    all_companies
elif choice == "Login":
    st.subheader("Login")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):
        hashed_pwd = make_hashes(password)
        result = login(username, hashed_pwd)
        if result:
            st.success("Logged In as {}".format(username))
            task = st.selectbox("Task",["Add Post","Analytics","Profiles"])
            if task == "Add Post":
                st.subheader("Add Your Post")

            elif task == "Analytics":
                st.subheader("Analytics")
            elif task == "Profiles":
                st.subheader("User Profiles")
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
                st.dataframe(clean_db)
        else:
            st.warning("Incorrect Username/Password")
elif choice == "Sign Up":
    st.subheader("Create New Account")
    
    username = st.text_input("* Username")
    password = st.text_input("* Password", type='password')
    email = st.text_input("E-mail")
    age = st.text_input("Age")
    gender = st.selectbox("Gender", ["M", "F"])

    if st.button("Sign Up"):
        register(username, make_hashes(password), age, gender, email)
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")
