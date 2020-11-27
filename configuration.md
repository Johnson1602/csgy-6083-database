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
- psql -h localhost -U wx650 project_db

## add data into tables
- \copy companies from '/Users/johnson/Downloads/Companies.csv' with delimiter ',' csv header;

## sql queries (with join or group by)
- 某个制造商生产的所有产品：Devices join Manufactures
- 查看评分（AVG）在某区间内的产品：Devices join Reviews
- 查看产品的评价：Devices join Reviews join Users
- 查看经销商销售额：Retailers join Sales join Retailers_Sale
- 年度销量（SUM）榜：Devices join Retailers join Sales join Retailers_Sale

## Tomorrow: 
- retailer_sales table
- update schema.sql(Supplier,Collaborate)
- update ER