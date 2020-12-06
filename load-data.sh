cat data/Companies.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY companies from STDIN CSV HEADER"
cat data/Devices.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY devices from STDIN CSV HEADER"
cat data/Suppliers.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY suppliers from STDIN CSV HEADER"
cat data/Produce.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY produce from STDIN CSV HEADER"
cat data/Collaborate.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY collaborate from STDIN CSV HEADER"
cat data/Retailers.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY retailers from STDIN CSV HEADER"
psql -d project_db -a -f /home/wx650/project/data/Sales.sql
cat data/Retailers_sale.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY retailers_sale from STDIN CSV HEADER"
cat data/Stores.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY stores from STDIN CSV HEADER"
cat data/Users.csv | psql -U wx650 -d project_db -h localhost -p 5432 -c "COPY users from STDIN CSV HEADER"
psql -d project_db -a -f /home/wx650/project/data/Reviews.sql