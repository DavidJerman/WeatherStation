from pytz import timezone
import datetime
import sqlite3
import os
import matplotlib
matplotlib.use('Agg')
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
    # Air
    for file in os.listdir("static/air_plots"):
        os.remove("./static/air_plots/" + file)

    # Connection
    connection = sqlite3.connect("dataGrabber/database.sqlite3")

    # Make sure that there are enough measurements
    found = False
    result = connection.execute(f"SELECT temp FROM data WHERE STRFTIME('%H', date) = {2} AND"
                                f" STRFTIME('%d', date) = {day}")
    for _ in result:
        found = True
        break

    # Determine the maximum hour
    max_range = 0
    for i in range(24):
        result = connection.execute(f"SELECT temp FROM data WHERE STRFTIME('%H', date) = {i} AND"
                                    f" STRFTIME('%d', date) = {day} AND STRFTIME('%M', date) > 54")
        for _ in result:
            max_range = i
            break

    # Plot making
    if found:
        # Temperature Plot
        temps = []
        for i in range(int(max_range)):
            result = connection.execute(f"SELECT temp FROM data WHERE STRFTIME('%H', date) = {i} AND"
                                        f" STRFTIME('%d', date) = {day}")
            for temp in result:
                temps.append(temp[0])
        temps = slope(temps, 400)

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
            result = connection.execute(f"SELECT humidity FROM data WHERE STRFTIME('%H', date) = {i} AND"
                                        f" STRFTIME('%d', date) = {day}")
            for hum in result:
                hums.append(hum[0])
        hums = slope(hums, 400)

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
            result = connection.execute(f"SELECT light FROM data WHERE STRFTIME('%H', date) = {i} AND"
                                        f" STRFTIME('%d', date) = {day}")
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

        # Air Pollution Plot
        airs = []
        for i in range(int(max_range)):
            result = connection.execute(f"SELECT air FROM data WHERE STRFTIME('%H', date) = {i} AND"
                                        f" STRFTIME('%d', date) = {day}")
            for air in result:
                airs.append(air[0])
        airs = slope(airs, 50)

        x = np.linspace(0.0, max_range + 1, len(airs))
        y = np.array(airs)
        plt.plot(x, y)
        plt.title("Air Pollution Levels")
        plt.ylabel("Air Pollution Level [ppm]")
        plt.xlabel("Hours [h]")
        plt.savefig(f"./static/air_plots/plot{name}.jpg")
        plt.close()

        picture = Image.open(f"static/air_plots/plot{name}.jpg")
        picture.save(f"./static/air_plots/plot_compressed{name}.jpg", optimize=True, quality=60)
        os.remove(f'static/air_plots/plot{name}.jpg')

        # Pressure Plot
        # TODO: Sensor to be added, different units, this is just temporary
        # pressures = []
        # for i in range(int(max_range)):
        #     result = connection.execute(f"SELECT temp FROM data WHERE STRFTIME('%H', date) = {i} AND"
        #                                 f" STRFTIME('%d', date) = {day}")
        #     for pressure in result:
        #         pressures.append(pressure[0])
        # pressures = slope(pressures, 400)
        #
        # x = np.linspace(0.0, max_range + 1, len(pressures))
        # y = np.array(pressures)
        # plt.plot(x, y)
        # plt.title("Pressure Levels")
        # plt.ylabel("Pressure [kPa]")
        # plt.xlabel("Hours [h]")
        # plt.savefig(f"./static/pressure_plots/plot{name}.jpg")
        # plt.close()
        #
        # picture = Image.open(f"static/pressure_plots/plot{name}.jpg")
        # picture.save(f"./static/pressure_plots/plot_compressed{name}.jpg", optimize=True, quality=60)
        # os.remove(f'static/pressure_plots/plot{name}.jpg')

        connection.close()

        global counter
        counter += 1
        print("Plots created: ", counter)

    else:
        raise Exception


def slope(source, slope_range):
    if len(source) > 600:
        # Average the data/plot
        avgs = []
        # Adding the missing data at the start
        for i in range(int(slope_range/2)):
            _sum = 0
            c = 0
            for j in range(i + 1):
                _sum += source[i - j]
                _sum += source[i + j]
                c += 2
            avgs.append(_sum/c)
        # Averaging the data
        for i in range(int(slope_range/2), len(source) - int(slope_range/2) - 1):
            _sum = 0
            for j in range(int(slope_range/2)):
                _sum += float(source[-j + i])
                _sum += float(source[j + i])
            avgs.append(_sum/slope_range)
        # Adding the missing data at the end
        for i in range(int(slope_range/2), -1, -1):
            _sum = 0
            c = 0
            for j in range(i + 1):
                _sum += source[len(source) - (i - j) - 1]
                _sum += source[len(source) - (i + j) - 1]
                c += 2
            avgs.append(_sum/c)
        return avgs
    else:
        return source


if __name__ == "__main__":
    while True:
        try:
            create_plot()
        except:
            print("Failed to crate a plot, will retry in 600 seconds.")
        sleep(600)
