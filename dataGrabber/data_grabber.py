import sqlite3
from serial import Serial
import datetime
from pytz import timezone
from time import sleep

print("Started collecting data...")

# Serial connection
serial_connection = Serial('/dev/ttyACM0')

# Sqlite3 connection
connection = sqlite3.connect('database.sqlite3')
cursor = connection.cursor()

# Create table if not exists
cursor.execute(f'''CREATE TABLE IF NOT EXISTS data (light float NOT NULL, water float NOT NULL, temp float NOT NULL,
                   humidity float NOT NULL, pressure float NOT NULL, air float NOT NULL, date date PRIMARY KEY)''')
connection.commit()


def delete_old_data():
    # Deleting old data
    cursor.execute(f'''SELECT STRFTIME('%Y', date), STRFTIME('%m', date), STRFTIME('%d', date) FROM data''')
    current_year = int(datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%Y"))
    current_month = int(datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%m"))
    current_day = int(datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%d"))
    for data_point in cursor.fetchall():
        _year, _month, _day = data_point
        if _year == current_year:
            if _month == current_month:
                if current_day - _day < 3:
                    continue
        cursor.execute(f'''DELETE FROM data WHERE {_year} == STRFTIME('%Y', date) AND {_month} == STRFTIME('%m', date)
         AND {_day} == STRFTIME('%d', date)''')


delete_old_data()
c = 0
c4 = 0
while True:
    try:
        c += 1
        c4 += 1
        line = str(serial_connection.readline())
        print(line)
        # Get the date
        date = datetime.datetime.now(tz=timezone('Europe/Ljubljana'))
        year = date.strftime("%Y")
        month = date.strftime("%m")
        day = date.strftime("%d")
        hour = date.strftime("%H")
        minute = date.strftime("%M")
        second = date.strftime("%S")
        timestamp = '{0:0>4s}-{1:0>2s}-{2:0>2s} {3:0>2s}:{4:0>2s}:{5:0>2s}'.format(year, month, day, hour, minute,
                                                                                   second)
        # Get values from the arduino data
        light = float(line.split("light:[")[1].split("]")[0]) * 100
        water = float(line.split("water:[")[1].split("]")[0])
        temp = float(line.split("temp:[")[1].split("]")[0])
        humidity = float(line.split("humidity:[")[1].split("]")[0])
        pressure = float(line.split("pressure:[")[1].split("]")[0])  # TODO: Sensor to be installed
        air = float(line.split("air:[")[1].split("]")[0])  # TODO: Sensor to be installed
        if temp < 0:
          temp += 3276.8
          temp = -temp
        # Insert into the database
        cursor.execute(f'''INSERT INTO data
         VALUES ({light}, {water}, {temp}, {humidity}, {pressure}, {air}, {timestamp})''')
        connection.commit()
        # Delete old data (older than 3 days)
        if c == 1000:
            delete_old_data()
            c = 0
    except IndexError:
        print("Index error, trying to re-measure")
        sleep(2)
    except:
        pass
    finally:
        print("Collected: " + str(c4))
