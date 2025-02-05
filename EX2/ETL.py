import pandas as pd
import mysql.connector

data = pd.read_csv('02_Hotspot_Data_Ex.csv', encoding='TIS-620')

columns = ['LATITUDE', 'LONGITUDE', 'DATE', 'TIME', 'CONFIDENCE', 'TUMBOON', 'AUMPER', 'PROVINCE', 'NAME']
data = data[columns]
filter = data[(data['NAME'] == 'เกษตรกรรม') & (data['CONFIDENCE'] > 50)]
filter['DATE'] = pd.to_datetime(data['DATE'], format='%d/%m/%Y',).dt.strftime('%Y-%m-%d')
filter['TIME'] = pd.to_datetime(data['TIME'], format='%H%M',).dt.strftime('%H:%M:%S')
print(filter)

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
)
db_cursor = connection.cursor()
db_cursor.execute("CREATE DATABASE Ex02")
db_cursor.execute("USE Ex02")
db_cursor.execute("""
    CREATE TABLE Hotspot_Data (
        LATITUDE FLOAT,
        LONGITUDE FLOAT,
        DATE DATE,
        TIME TIME,
        CONFIDENCE INT,
        TUMBOON VARCHAR(255),
        AUMPER VARCHAR(255),
        PROVINCE VARCHAR(255),
        NAME VARCHAR(255),
        IMPORTED_DATETIME TIMESTAMP
    )
""")

for i, row in filter.iterrows():
    db_cursor.execute("""
        INSERT INTO Hotspot_Data (LATITUDE, LONGITUDE, DATE, TIME, CONFIDENCE, TUMBOON, AUMPER, PROVINCE, NAME, IMPORTED_DATETIME)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
    """, (row['LATITUDE'], row['LONGITUDE'], row['DATE'], row['TIME'], row['CONFIDENCE'], row['TUMBOON'], row['AUMPER'], row['PROVINCE'], row['NAME']))
connection.commit()
db_cursor.close()
connection.close()


