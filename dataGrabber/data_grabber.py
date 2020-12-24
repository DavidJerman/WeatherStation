import sqlite3
from serial import Serial
import datetime

print("Started collecting data...")

# Serial connection
serial_connection = Serial('COM4')

# Sqlite3 connection
connection = sqlite3.connect('database.sqlite3')
cursor = connection.cursor()

# Create table if not exists
cursor.execute(f'''CREATE TABLE IF NOT EXISTS data (light float, water float, temp float, humidity float,
 year int, month int, day int, hour int, minute int, second int,
 PRIMARY KEY (year, month, day, hour, minute, second))
 ''')
connection.commit()


def delete_old_data():
    cursor.execute(f'''SELECT year, month, day FROM data''')
    current_year = int(datetime.datetime.now().strftime("%Y"))
    current_month = int(datetime.datetime.now().strftime("%m"))
    current_day = int(datetime.datetime.now().strftime("%d"))
    for data_point in cursor.fetchall():
        _year, _month, _day = data_point
        if _year == current_year:
            if _month == current_month:
                if current_day - _day < 3:
                    continue
        cursor.execute(f'''DELETE FROM data WHERE {_year} == year AND {_month} == month AND {_day} == day''')


delete_old_data()
c = 0
while True:
    c += 1
    line = str(serial_connection.readline())
    date = datetime.datetime.now()
    year = int(date.strftime("%Y"))
    month = int(date.strftime("%m"))
    day = int(date.strftime("%d"))
    hour = int(date.strftime("%H"))
    minute = int(date.strftime("%M"))
    second = int(date.strftime("%S"))
    light = float(line.split("light:[")[1].split("]")[0])
    water = float(line.split("water:[")[1].split("]")[0])
    temp = float(line.split("temp:[")[1].split("]")[0])
    humidity = float(line.split("humidity:[")[1].split("]")[0])
    cursor.execute(f'''INSERT INTO data
     VALUES ({light}, {water}, {temp}, {humidity}, {year}, {month}, {day}, {hour}, {minute}, {second})''')
    connection.commit()
    if c == 1000:
        delete_old_data()
        c = 0