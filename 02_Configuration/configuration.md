## project environment (cloud)
- Python (3.6.8)
- Streamlit (0.64.0)
- PosgreSQL (12.1)
- pandas (1.1.0)
- psycopg2 (2.7.5)

## project environment (local)
- Python (3.7.4)
- Streamlit (0.71.0)
- PosgreSQL (12.4)
- pandas (1.1.4)
- psycopg2-binary (2.8.6)
- SSL port number: 8548

## commands
- connect to database (cloud): psql -h localhost -U wx650 project_db
- create tables: \i '/Users/johnson/Downloads/Project/schema.sql'
- add data into tables (local)
	- \copy companies from '/Users/johnson/Downloads/Project/data/Companies.csv' with delimiter ',' csv header;
	- \copy devices from '/Users/johnson/Downloads/Project/data/Devices.csv' with delimiter ',' csv header;
	- \copy suppliers from '/Users/johnson/Downloads/Project/data/Suppliers.csv' with delimiter ',' csv header;
	- \copy produce from '/Users/johnson/Downloads/Project/data/Produce.csv' with delimiter ',' csv header;
	- \copy collaborate from '/Users/johnson/Downloads/Project/data/Collaborate.csv' with delimiter ',' csv header;
	- \copy retailers from '/Users/johnson/Downloads/Project/data/Retailers.csv' with delimiter ',' csv header;
	- \i '/Users/johnson/Downloads/Project/data/Sales.sql'
	- \copy retailers_sale from '/Users/johnson/Downloads/Project/data/Retailers_sale.csv' with delimiter ',' csv header;
	- \copy stores from '/Users/johnson/Downloads/Project/data/Stores.csv' with delimiter ',' csv header;
- add data into tables (cloud)
	- \copy companies from '/home/wx650/project/data/Companies.csv' with delimiter ',' csv header;
	- \copy devices from '/home/wx650/project/data/Devices.csv' with delimiter ',' csv header;
	- \copy suppliers from '/home/wx650/project/data/Suppliers.csv' with delimiter ',' csv header;
	- \copy produce from '/home/wx650/project/data/Produce.csv' with delimiter ',' csv header;
	- \copy collaborate from '/home/wx650/project/data/Collaborate.csv' with delimiter ',' csv header;
	- \copy retailers from '/home/wx650/project/data/Retailers.csv' with delimiter ',' csv header;
	- \i '/home/wx650/project/data/Sales.sql'
	- \copy retailers_sale from '/home/wx650/project/data/Retailers_sale.csv' with delimiter ',' csv header;
	- \copy stores from '/home/wx650/project/data/Stores.csv' with delimiter ',' csv header;
	- \copy users from '/home/wx650/project/data/Users.csv' with delimiter ',' csv header;
	- \i '/home/wx650/project/data/Reviews.sql'

## sql queries (with join or group by)
- 某个制造商生产的所有产品：Devices join Manufactures
- 查看评分（AVG）在某区间内的产品：Devices join Reviews
- 查看产品的评价：Devices join Reviews join Users
- 查看经销商销售额：Retailers join Sales join Retailers_Sale
- 年度销量（SUM）榜：Devices join Retailers join Sales join Retailers_Sale

## Tomorrow
- retailer_sales table - done
- update schema.sql(Supplier,Collaborate) - done
- update ER - done

## Keep Streamlit App Running
- ssh -L logon to gauss server
- cd project folder: $ cd project/
- launch a new tmux session: $ tmux
- run the app: $ streamlit run project.py --server.address=localhost --server.port=8548
- detach from the tmux session by using ctrl + b, then d
- In another terminal, you can use the following command to check running status or terminate the app
	- show streamlit process information: $ ps -u wx650 | grep streamlit
	- kill the process: $ kill [PID]