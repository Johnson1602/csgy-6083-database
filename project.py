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
    st.dataframe(all_companies)
    
    tasks = ["List All devices produced by a particular supplier",
            "View devices that AVG score within a particular range",
            "List all reviews of a product",
            "View all sales of a particular retailer",
            "List the sales of devices in descending order"]
    functions = st.selectbox("Functions", tasks)
    if functions == tasks[0]:
        st.subheader("List All devices produced by a particular supplier")
        sql_suppliers = "select name from Suppliers;"
        suppliers = query_db(sql_suppliers)['name'].tolist()
        supplier_sel = st.selectbox('choose a supplier', suppliers)
        if supplier_sel:
            sql_devices = f"select * from devices d, suppliers s,produce p where d.name = p.D_name and d.launch_date = p.launch_date and p.M_name='{supplier_sel}';"
            devices = query_db(sql_devices)
            st.dataframe(devices)
    
    # elif function == tasks[1]:
    #     st.subheader("View devices that AVG score within a particular range")
    #     sql_devices = f'select d.name, d.launch_date, sum(r.rating)/count(*) as avg_rating from devices d,reviews r where d.name = r.D_name and d.launch_date = r.launch_date groupy by d.name,d.launch_date having avg_rating >= {left} and avg_rating <= {right};'
    #     devices = query_db(sql_devices)
    #     st.dataframe(devices)
        
    elif functions == tasks[2]:
        st.subheader("List all reviews of a product")
        sql_devices = "select name from devices;"
        devices = query_db(sql_devices)['name'].tolist()
        device_sel = st.selectbox('choose a device', devices)
        if device_sel:
            sql_reviews = f"select D_name as name, launch_date, rating, time, U_name, content from reviews where D_name = '{device_sel}';"
            reviews = query_db(sql_reviews)
            st.dataframe(reviews)
            
    elif functions == tasks[3]:
        st.subheader("View all sales of a particular retailer")
        sql_retailers = 'select name from retailers;'
        retailers = query_db(sql_retailers)['name'].tolist()
        retailer_sel = st.selectbox('choose a retailer', retailers)
        if retailer_sel:
            sql_sales = f"select r.sid, r.D_name as name, r.launch_date, s.year, s.season, s.quantity from sales s, Retailers_Sale r where r.R_name = '{retailer_sel}' and r.sid = s.id;"
            sales = query_db(sql_sales)
            st.dataframe(sales)
        
    elif functions == tasks[4]:
        st.subheader("List the sales of devices in descending order")
        sql_devices = "select name from devices;"
        devices = query_db(sql_devices)['name'].tolist()
        device_sel = st.selectbox('choose a device', devices)
        if device_sel:
            sql_sales = f"select r.D_name as name, r.launch_date, sum(s.quantity) as quantity from Retailers_Sale r, sales s where r.D_name = '{device_sel}' and r.sid = s.id group by r.D_name order by sum(s.quantity) desc;"
            sales = query_db(sql_sales)
            st.dataframe(sales)
        
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
