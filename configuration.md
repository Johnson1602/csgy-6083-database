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
- add data into tables
	- \copy companies from '/Users/johnson/Downloads/Project/data/Companies.csv' with delimiter ',' csv header;
	- \copy devices from '/Users/johnson/Downloads/Project/data/Devices.csv' with delimiter ',' csv header;
	- \copy suppliers from '/Users/johnson/Downloads/Project/data/Suppliers.csv' with delimiter ',' csv header;
	- \copy produce from '/Users/johnson/Downloads/Project/data/Produce.csv' with delimiter ',' csv header;
	- \copy collaborate from '/Users/johnson/Downloads/Project/data/Collaborate.csv' with delimiter ',' csv header;
	- \copy retailers from '/Users/johnson/Downloads/Project/data/Retailers.csv' with delimiter ',' csv header;
	- \i '/Users/johnson/Downloads/Project/data/Sales.sql'
	- \copy retailers_sale from '/Users/johnson/Downloads/Project/data/Retailers_sale.csv' with delimiter ',' csv header;
	- \copy stores from '/Users/johnson/Downloads/Project/data/Stores.csv' with delimiter ',' csv header;

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