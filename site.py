import datetime
from pytz import timezone
from flask import Flask, render_template
from PIL import Image
import sqlite3
import os
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def website():
    date = datetime.datetime.now(tz=timezone('Europe/Ljubljana'))
    date = date.strftime("%d-%m-%Y %H:%M:%S")
    temp, moisture, water, sunlight = get_data()
    img_name = ""
    plot_name = ""
    create_plot()
    for file in os.listdir('static/imgs'):
        img_name = file
    for file in os.listdir('static/plots'):
        plot_name = file
    return render_template(template_name_or_list='index.html', date=date, temp=str(temp) + " °C",
                           moisture=str(moisture) + "%", sunlight=str(sunlight) + " %",
                           image=os.path.join('static/imgs', img_name), plot=os.path.join('static/plots', plot_name))


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
            connection.close()
            return round(temp_avg, 1), round(humidity_avg, 1), round(water_avg*100, 1), round(light_avg*100, 1)


def create_plot():
    year, month, day, hour, minute = datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%Y"), datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%m"), \
                                     datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%d"), datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%H"), \
                                     datetime.datetime.now(tz=timezone('Europe/Ljubljana')).strftime("%M")
    for file in os.listdir("static/plots"):
        os.remove("./static/plots/" + file)
    name = "_" + year + "_" + month + "_" + day + "_" + hour + "_" + minute

    connection = sqlite3.connect("dataGrabber/database.sqlite3")
    # result = connection.execute(f"SELECT temp FROM data WHERE day = {day}")
    # temps = []
    # for temp in result:
    #     temps.append(temp[0])

    temps = []
    for i in range(int(hour) + 1):
        _sum = 0
        result = connection.execute(f"SELECT temp FROM data WHERE hour = {i} AND day = {day}")
        c = 0
        for temp in result:
            _sum += temp[0]
            c += 1
        if c == 0:
            continue
        _sum /= c
        temps.append(_sum)

    # plt.plot(slope(temps, 100))
    plt.plot(temps)
    plt.title("Temperatures")
    plt.ylabel("Temperature [C]")
    plt.xlabel("Hours [h]")
    plt.savefig(f"./static/plots/plot{name}.jpg")
    plt.close()

    picture = Image.open(f"./static/plots/plot{name}.jpg")
    picture.save(f"./static/plots/plot_compressed{name}.jpg", optimize=True, quality=60)
    os.remove(f'./static/plots/plot{name}.jpg')
    print("Plot created")
    connection.close()


def slope(source, slope_range):
    avgs = []
    for i in range(int(slope_range/2), len(source) - int(slope_range/2) - 1):
        sum = 0
        for j in range(int(slope_range/2)):
            sum += float(source[-j + i])
            sum += float(source[j + i])
        avgs.append(sum/slope_range)
    return avgs


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
