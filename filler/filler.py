import mysql.connector as connector
from time import sleep


with open("/data/data.csv", 'r') as f:
    data = f.readlines()

data = list(map(str.strip, data))
data = list(map(lambda x: x.split(','), data))

sleep(10)

db = connector.connect(
    user='user', password='userpwd',
    host='db', port=3306,
    database='main'
)

cursor = db.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS main (
    id INT NOT NULL AUTO_INCREMENT,
    data TEXT NOT NULL,
    val FLOAT NOT NULL,
    PRIMARY KEY (id) )""")

insert_st = "INSERT INTO main (data, val) VALUES (%s, %s)"
cursor.executemany(insert_st, data)
db.commit()
