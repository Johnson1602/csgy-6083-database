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

# Sidebar
# Places
place = st.sidebar.radio("Places", ('Home', 'Advanced Query', 'Review'))
# Account
choice = st.sidebar.selectbox("Account", ("Login", "Sign Up"))

# Security
import hashlib
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# register new user
def register(username, password, age, gender, email):
    db_info = get_config()
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    # check duplicate username
    check_is_exist = f"select * from users where username = '{username}';"
    query_db(check_is_exist)
    if not query_db(check_is_exist).empty:
        return False
    else: 
        add_user = f"insert into users (username, age, gender, password, email) values ('{username}', {age}, '{gender}', '{password}', '{email}');"
        cur.execute(add_user)
        conn.commit()
    cur.close()
    conn.close()
    return True

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

# Places
if place == "Home":
    st.header("Home")
    "Here are all the data we have"

    # devices
    st.subheader("Devices")
    query_all_devicees = "select name, C_name as company, launch_date, type, price, capacity, chip, camera, battery, dimension, screen_size, weight, os from devices;"
    all_devicees = query_db(query_all_devicees)
    all_devicees

    # reviews
    st.subheader("Device Reviews")
    query_all_reviews = "select time, d_name as device, rating, content as comment, u_name as user from reviews;"
    all_reviews = query_db(query_all_reviews)
    all_reviews

    # companies
    st.subheader("Companies")
    query_all_companies = "select * from companies;"
    all_companies = query_db(query_all_companies)
    all_companies

    # suppliers
    st.subheader("Suppliers")
    query_all_suppliers = "select * from suppliers;"
    all_suppliers = query_db(query_all_suppliers)
    all_suppliers

    # retailers
    st.subheader("Retailers")
    query_all_retailers = "select * from retailers;"
    all_retailers = query_db(query_all_retailers)
    all_retailers

    # stores
    st.subheader("Stores")
    query_all_stores = "select id as store_id, R_name as retailer, address, operation_time, contact_number from stores;"
    all_stores = query_db(query_all_stores)
    all_stores

    # sales
    st.subheader("Sales")
    query_all_sales = """select RS.r_name as retailer, S.year, S.season, RS.d_name as device, S.quantity
                         from retailers_sale as RS, sales as S
                         where RS.sid = S.id
                         order by S.year, S.season, S.quantity"""
    all_sales = query_db(query_all_sales)
    all_sales
elif place == "Advanced Query":
    st.header("Advanced Query")
    "Here you can perform some advanced queries"
    tasks = ["List All devices produced by a particular supplier",
            "View devices that AVG score within a particular range",
            "List all products from a specific price range",
            "List all reviews of a product",
            "View all sales of a particular retailer",
            "List the sales of devices in descending order",
            "List all products from chosen companies"]
    functions = st.selectbox("Queries", tasks)
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
        st.subheader("List all products from a specific price range")
        start_price, end_price = st.slider('Select price range', 0.0, 2000.0, (500.0, 1000.0))
        sql_devices = f'select name, C_name as company, launch_date, type, price, capacity, chip, camera, battery, dimension, screen_size, weight, os from devices where price >= {start_price} and price <= {end_price};'
        devices = query_db(sql_devices)
        st.dataframe(devices)
    elif functions == tasks[3]:
        st.subheader("List all reviews of a product")
        sql_devices = "select name from devices;"
        devices = query_db(sql_devices)['name'].tolist()
        device_sel = st.selectbox('choose a device', devices)
        if device_sel:
            sql_reviews = f"select D_name as name, rating, time, U_name, content from reviews where D_name = '{device_sel}';"
            reviews = query_db(sql_reviews)
            st.dataframe(reviews)
    elif functions == tasks[4]:
        st.subheader("View all sales of a particular retailer")
        sql_retailers = 'select name from retailers;'
        retailers = query_db(sql_retailers)['name'].tolist()
        retailer_sel = st.selectbox('choose a retailer', retailers)
        if retailer_sel:
            sql_sales = f"select r.D_name as name, s.year, s.season, s.quantity from sales s, Retailers_Sale r where r.R_name = '{retailer_sel}' and r.sid = s.id;"
            sales = query_db(sql_sales)
            st.dataframe(sales)
    elif functions == tasks[5]:
        st.subheader("List the sales of devices in descending order")
        sql_year = "select distinct year from sales;"
        years = query_db(sql_year)['year'].tolist()
        year_sel = st.selectbox('choose a year', years)
        if year_sel:
            sql_sales = f"select r.D_name as name, sum(s.quantity) as quantity from Retailers_Sale r, sales s where s.year = '{year_sel}' and r.sid = s.id group by r.D_name order by sum(s.quantity) desc;"
            sales = query_db(sql_sales)
            st.dataframe(sales)
    elif functions == tasks[6]:
        st.subheader("List all products from chosen companies")
        sql_companies = "select name from companies;"
        companies = query_db(sql_companies)['name'].tolist()
        company_mulsel = st.multiselect('Choose companies', companies)
        if company_mulsel:
            company_str = ','.join(["'" + company + "'" for company in company_mulsel])
            # print(dates_str)
            sql_device = f"""select name, c_name as company
                             from devices
                             where c_name in ({company_str})"""
            result = query_db(sql_device)
            st.dataframe(result)

# Account
if choice == "Login":
    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password", type='password')
    if st.sidebar.checkbox("Login"):
        hashed_pwd = make_hashes(password)
        result = login(username, hashed_pwd)
        if result:
            # login successful prompt
            st.sidebar.success("Logged In as {}".format(username))

            if place == "Review":
                st.header("Review")
                "Here you can find all your past reviews or write a new review"
                func = st.selectbox("Action", ('Your Reviews', 'Write A New Review'))
                if func == "Your Reviews":
                    st.subheader("Your Reviews")
                    query_all_reviews = f"select time, d_name as device, rating, content as comment from reviews where u_name = '{username}';"
                    all_reviews = query_db(query_all_reviews)
                    all_reviews
                elif func == "Write A New Review":
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
                        query_all_reviews = f"select time, d_name as device, rating, content as comment from reviews where u_name = '{username}';"
                        all_reviews = query_db(query_all_reviews)
                        st.dataframe(all_reviews)
        else:
            st.warning("Incorrect Username/Password")
elif choice == "Sign Up":
    username = st.sidebar.text_input("* Username")
    password = st.sidebar.text_input("* Password", type='password')
    email = st.sidebar.text_input("* E-mail")
    age = st.sidebar.text_input("* Age")
    gender = st.sidebar.selectbox("Gender", ["M", "F"])

    if st.sidebar.button("Sign Up"):
        if username == "" or password == "" or email == "" or age == "":
            st.sidebar.warning('Please enter all information')
        else:
            if register(username, make_hashes(password), age, gender, email):
                st.sidebar.success("Success")
            else:
                st.sidebar.warning('Please choose another username and try again')
