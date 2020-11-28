import pandas as pd
import datetime
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
# @st.cache
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

menu = ["Home", "Login", "Sign Up"]
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

# new comment
def new_comment(content, rating, d_name, u_name):
    db_info = get_config()
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")
    cur.execute('insert into reviews (content, rating, time, d_name, u_name) values (%s, %s, %s, %s, %s);', (content, rating, current_time, d_name, u_name))
    conn.commit()
    cur.close()
    conn.close()

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
            sql_devices = f"select d.name,launch_date,type,price,capacity,chip,camera,battery,dimension,screen_size,weight,os from devices d, produce p where d.name = p.D_name and p.M_name='{supplier_sel}';"
            devices = query_db(sql_devices)
            st.dataframe(devices)
    
    elif functions == tasks[1]:
        st.subheader("View devices that AVG score within a particular range")
        start_rating, end_rating = st.select_slider('Select a range of ratings', options=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5],value=(3.5, 4.5))
        sql_devices = f'select d.name, d.launch_date, sum(r.rating)/count(*) as avg_rating from devices d,reviews r where d.name = r.D_name group by d.name having sum(r.rating)/count(*) >= {start_rating} and sum(r.rating)/count(*) <= {end_rating};'
        devices = query_db(sql_devices)
        st.dataframe(devices)
        
    elif functions == tasks[2]:
        st.subheader("List all reviews of a product")
        sql_devices = "select name from devices;"
        devices = query_db(sql_devices)['name'].tolist()
        device_sel = st.selectbox('choose a device', devices)
        if device_sel:
            sql_reviews = f"select D_name as name, rating, time, U_name, content from reviews where D_name = '{device_sel}';"
            reviews = query_db(sql_reviews)
            st.dataframe(reviews)
            
    elif functions == tasks[3]:
        st.subheader("View all sales of a particular retailer")
        sql_retailers = 'select name from retailers;'
        retailers = query_db(sql_retailers)['name'].tolist()
        retailer_sel = st.selectbox('choose a retailer', retailers)
        if retailer_sel:
            sql_sales = f"select r.D_name as name, s.year, s.season, s.quantity from sales s, Retailers_Sale r where r.R_name = '{retailer_sel}' and r.sid = s.id;"
            sales = query_db(sql_sales)
            st.dataframe(sales)
        
    elif functions == tasks[4]:
        st.subheader("List the sales of devices in descending order")
        sql_year = "select distinct year from sales;"
        years = query_db(sql_year)['year'].tolist()
        year_sel = st.selectbox('choose a year', years)
        if year_sel:
            sql_sales = f"select r.D_name as name, sum(s.quantity) as quantity from Retailers_Sale r, sales s where s.year = '{year_sel}' and r.sid = s.id group by r.D_name order by sum(s.quantity) desc;"
            sales = query_db(sql_sales)
            st.dataframe(sales)

elif choice == "Login":
    # st.subheader("Login")
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):
        hashed_pwd = make_hashes(password)
        result = login(username, hashed_pwd)
        if result:
            # login successful prompt
            st.success("Logged In as {}".format(username))

            # write new review
            st.subheader("Write A New Review")

            query_all_devices = 'select name from devices;'
            all_devices = query_db(query_all_devices)['name'].tolist()

            select_device = st.selectbox('Please choose a device', all_devices)
            rating = st.select_slider('Overall rating', options=[0, 1, 2, 3, 4, 5])
            comments = st.text_area('Your comments')

            # submit new comment
            if st.button("Submit"):
                new_comment(comments, rating, select_device, username)
                st.success("You have successfully added a new product review")

                # past reviews
                st.subheader("Your Reviews")
                query_all_reviews = f"select time, d_name as Device, rating, content as Comment from reviews where u_name = '{username}';"
                all_reviews = query_db(query_all_reviews)
                st.dataframe(all_reviews)

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
