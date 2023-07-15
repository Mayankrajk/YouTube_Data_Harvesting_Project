import collections

import seaborn as sns
from pymongo import MongoClient
import mysql.connector

df=sns.load_dataset('tips')
df=df.head(10)
print(df)

client=MongoClient("mongodb://localhost:27017")
print(client.test)
print(client.list_database_names())
print()

df.reset_index(inplace=True)

data=df.to_dict('records')
print(data)
print("------------")


new_db=client['youtube']
print(client.list_database_names())
new_col=new_db['channel']
new_col.insert_many(data)


print(client.list_database_names())

con = mysql.connector.connect(host="localhost", user="root", password="Ashu@123", database="youtube")
print(con)
cursor=con.cursor()
print(cursor.execute("show databases"))

#cursor.execute("create database youtube")

#cursor.execute("create table hotel(index varchar(20), total_bill varchar(40), tip varchar(40), sex varchar(40), smoker varchar(20), day varchar(30), time varchar(20), size varchar(40))")


#cursor.execute("create table hotel(index varchar(20), total_bill varchar(20), tip varchar(20), sex varchar(20), smoker varchar(20), day varchar(20), time varchar(20), size varchar(20))")







# Iterate over the MongoDB data and insert into MySQL table
for document in data:
    index = document['index']
    total_bill = document['total_bill']
    tip = document['tip']
    sex = document['sex']
    smoker = document['smoker']
    day = document['day']
    time = document['time']
    size = document['size']

    # Insert data into MySQL table
    sql_query = "INSERT INTO your_mysql_table (index, total_bill, tip, sex, smoker, day, time, size) VALUES (%s, %s, " \
                "%s, %s, %s, %s, %s, %s)"
    values = (index, total_bill, tip, sex, smoker, day, time, size)
    cursor.execute(sql_query, values)


# Commit the changes and close the connections
con.commit()
cursor.close()
con.close()
client.close()


















'''for document in data:
    query = """
        INSERT INTO hotel (`index`, total_bill, tip, sex, smoker, day, time, size)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
    values = (
        document['index'],
        document['total_bill'],
        document['tip'],
        document['sex'],
        document['smoker'],
        document['day'],
        document['time'],
        document['size']
    )
    cursor.execute(query, values)

    # Commit the changes and close the connection
'''








