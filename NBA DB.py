import pandas
from sqlalchemy import create_engine
import requests

# WAMP Database Info (create the nba database first)
hostname="127.0.0.1"
uname="root"
pwd=""
dbname="nba"

# Creating sqlalchemy engine object
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
            .format(host=hostname, db=dbname, user=uname, pw=pwd))

# Get data from API | https://www.analyticsvidhya.com/blog/2021/05/how-to-fetch-data-using-api-and-sql-databases/
url = 'https://www.balldontlie.io/api/v1/players?per_page=100'
response = requests.get(url)
r = response.json()["data"]

# Normalize JSON data into flat table (makes nested objects readable) | https://medium.com/swlh/converting-nested-json-structures-to-pandas-dataframes-e8106c59976e
data = pandas.json_normalize(r)
print(data)

# Make Pandas DataFrame table
df = pandas.DataFrame(data)[['id', 'first_name', 'height_feet', 'height_inches', 'last_name', 'position', 'team.name','weight_pounds']]

# Open connection to database and make table
connection=engine.connect()
df.to_sql('nba', con = engine, if_exists= 'replace')

# Close extension to database
connection.close()
