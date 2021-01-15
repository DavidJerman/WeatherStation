from pytz import timezone
import datetime
import sqlite3
import os
from matplotlib import pyplot as plt
from PIL import Image
from time import sleep
import numpy as np

counter = 0


def create_plot():
    # Time
    current_time = datetime.datetime.now(tz=timezone('Europe/Ljubljana'))
    year, month, day, hour, minute = current_time.strftime("%Y"), current_time.strftime("%m"),\
                                     current_time.strftime("%d"), current_time.strftime("%H"),\
                                     current_time.strftime("%M")

    name = "_" + year + "_" + month + "_" + day + "_" + hour + "_" + minute

    # Remove old plots
    # Temps
    for file in os.listdir("static/temp_plots"):
        os.remove("./static/temp_plots/" + file)
    # Humidity
    for file in os.listdir("static/humidity_plots"):
        os.remove("./static/humidity_plots/" + file)
    # Light
    for file in os.listdir("static/light_plots"):
        os.remove("./static/light_plots/" + file)

    # Connection
    connection = sqlite3.connect("dataGrabber/database.sqlite3")

    # Make sure that there are enough measurements
    found = False
    result = connection.execute(f"SELECT temp FROM data WHERE hour = 0 AND day = {day}")
    for _ in result:
        found = True
        break

    # Determine the maximum hour
    max_range = 0
    for i in range(24):
        result = connection.execute(f"SELECT temp FROM data WHERE hour = {i} AND day = {day} AND minute > 54")
        for _ in result:
            max_range = i
            break

    # Plot making
    if found:
        # Temperature Plot
        temps = []
        for i in range(int(max_range)):
            result = connection.execute(f"SELECT temp FROM data WHERE hour = {i} AND day = {day}")
            for temp in result:
                temps.append(temp[0])
        temps = slope(temps, 200)

        x = np.linspace(0.0, max_range + 1, len(temps))
        y = np.array(temps)
        plt.plot(x, y)
        plt.title("Temperature Levels")
        plt.ylabel("Temperature [C]")
        plt.xlabel("Hours [h]")
        plt.savefig(f"./static/temp_plots/plot{name}.jpg")
        plt.close()

        picture = Image.open(f"static/temp_plots/plot{name}.jpg")
        picture.save(f"./static/temp_plots/plot_compressed{name}.jpg", optimize=True, quality=60)
        os.remove(f'static/temp_plots/plot{name}.jpg')

        # Humidity Plot
        hums = []
        for i in range(int(max_range)):
            result = connection.execute(f"SELECT humidity FROM data WHERE hour = {i} AND day = {day}")
            for hum in result:
                hums.append(hum[0])
        hums = slope(hums, 200)

        x = np.linspace(0.0, max_range + 1, len(hums))
        y = np.array(hums)
        plt.plot(x, y)
        plt.title("Humidity Levels")
        plt.ylabel("Humidity [%]")
        plt.xlabel("Hours [h]")
        plt.savefig(f"./static/humidity_plots/plot{name}.jpg")
        plt.close()

        picture = Image.open(f"static/humidity_plots/plot{name}.jpg")
        picture.save(f"./static/humidity_plots/plot_compressed{name}.jpg", optimize=True, quality=60)
        os.remove(f'static/humidity_plots/plot{name}.jpg')

        # Light Level Plot
        lights = []
        for i in range(int(max_range)):
            result = connection.execute(f"SELECT light FROM data WHERE hour = {i} AND day = {day}")
            for light in result:
                lights.append(light[0])
        lights = slope(lights, 50)

        x = np.linspace(0.0, max_range + 1, len(lights))
        y = np.array(lights)
        plt.plot(x, y)
        plt.title("Light Levels")
        plt.ylabel("Light Level [%]")
        plt.xlabel("Hours [h]")
        plt.savefig(f"./static/light_plots/plot{name}.jpg")
        plt.close()

        picture = Image.open(f"static/light_plots/plot{name}.jpg")
        picture.save(f"./static/light_plots/plot_compressed{name}.jpg", optimize=True, quality=60)
        os.remove(f'static/light_plots/plot{name}.jpg')
        connection.close()

        global counter
        counter += 1
        print("Plots created: ", counter)


def slope(source, slope_range):
    avgs = []
    first = True
    for i in range(int(slope_range/2), len(source) - int(slope_range/2) - 1):
        sum = 0
        for j in range(int(slope_range/2)):
            sum += float(source[-j + i])
            sum += float(source[j + i])
        avgs.append(sum/slope_range)
        if first:
            first = False
            for _ in range(int(slope_range/2) - 1):
                avgs.append(sum/slope_range)
    for i in range(int(slope_range/2) - 1):
        avgs.append(avgs[len(avgs) - 1])
    return avgs


if __name__ == "__main__":
    while True:
        create_plot()
        sleep(600)
