import datetime
from pytz import timezone
from flask import Flask, render_template
import sqlite3
import os
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def website():
    date = datetime.datetime.now(tz=timezone('Europe/Ljubljana'))
    date = date.strftime("%d-%m-%Y %H:%M:%S")
    temp, moisture, water, sunlight = get_data()
    img_name = ""
    for file in os.listdir('static'):
        if file != "other":
            img_name = file
    return render_template(template_name_or_list='index.html', date=date, temp=str(temp) + " °C",
                           moisture=str(moisture) + "%", water=str(water) + " %", sunlight=str(sunlight) + " %",
                           image=os.path.join('static', img_name))


def get_data():
    connection = sqlite3.connect('dataGrabber/database.sqlite3')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT light, water, temp, humidity FROM data
                        ORDER BY year DESC, month DESC, day DESC, hour DESC, minute DESC''')
    c = 0
    light_avg = 0
    water_avg = 0
    temp_avg = 0
    humidity_avg = 0
    for data in cursor.fetchall():
        light, water, temp, humidity = data
        light_avg += light
        water_avg += water
        temp_avg += temp
        humidity_avg += humidity
        c += 1
        if c == 6:
            light_avg /= 6
            water_avg /= 6
            temp_avg /= 6
            humidity_avg /= 6
            return round(temp_avg, 1), round(humidity_avg, 1), round(water_avg*100, 1), round(light_avg*100, 1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
