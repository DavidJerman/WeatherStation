import datetime
from pytz import timezone
from flask import Flask, render_template, send_file
from shutil import copyfile
import sqlite3
import os
import zipfile

app = Flask(__name__)


@app.route("/")
@app.route("/index/")
def website():
    # Getting the datetime
    date = datetime.datetime.now(tz=timezone('Europe/Ljubljana'))
    date = date.strftime("%d-%m-%Y %H:%M:%S")
    # Data from database
    temp, moisture, sunlight = get_data()
    # Getting the plots
    img_name = ""
    temp_plot_name = ""
    humidity_plot_name = ""
    light_plot_name = ""
    air_plot_name = ""
    pressure_plot_name = ""
    for file in os.listdir('static/imgs'):
        img_name = file
    for file in os.listdir('static/temp_plots'):
        temp_plot_name = file
    for file in os.listdir('static/humidity_plots'):
        humidity_plot_name = file
    for file in os.listdir('static/light_plots'):
        light_plot_name = file
    for file in os.listdir('static/air_plots'):
        air_plot_name = file
    for file in os.listdir('static/pressure_plots'):
        pressure_plot_name = file
    # Returning the page to the user
    return render_template(template_name_or_list='index.html', date=date, temp=str(temp) + " °C",
                           moisture=str(moisture) + "%", sunlight=str(sunlight) + " %",
                           image=os.path.join('static/imgs', img_name),
                           temp_plot=os.path.join('static/temp_plots', temp_plot_name),
                           humidity_plot=os.path.join('static/humidity_plots', humidity_plot_name),
                           light_plot=os.path.join('static/light_plots', light_plot_name),
                           air_plot=os.path.join('static/air_plots', air_plot_name),
                           pressure_plot=os.path.join('static/pressure_plots', pressure_plot_name))


@app.route("/file-downloads/")
def download():
    # File download page
    try:
        return render_template(template_name_or_list='downloads.html')
    except Exception as e:
        return str(e)


@app.route("/about/")
def about():
    # About page
    try:
        return render_template(template_name_or_list='about.html')
    except Exception as e:
        return str(e)


@app.route("/return-files/")
def return_files_download():
    try:
        # Removing old files
        for file in os.listdir('dataGrabber/copy/'):
            os.remove('dataGrabber/copy/' + file)
        # Getting the date
        date = datetime.datetime.now(tz=timezone('Europe/Ljubljana'))
        date = date.strftime("%Y_%m_%d_%H_%M_%S")
        # Getting the file name
        filename = "database_" + date + ".sqlite3"
        path = os.path.join('dataGrabber/copy', filename)
        # Copying the current database
        copyfile('dataGrabber/database.sqlite3', path)
        # Getting the zip name
        zip_name = 'database_' + date + '.zip'
        zip_path = os.path.join('dataGrabber/copy', zip_name)
        # Zipping the copy
        zipfile.ZipFile(zip_path, mode='w').write(path)
        # Sending the file to the user
        return send_file(zip_path, as_attachment=True, attachment_filename=zip_name, cache_timeout=60)
    except Exception as e:
        return str(e)


def get_data():
    # Connecting to the sql database
    connection = sqlite3.connect('dataGrabber/database.sqlite3')
    cursor = connection.cursor()
    cursor.execute(f'''SELECT light, temp, humidity FROM data
                        ORDER BY year DESC, month DESC, day DESC, hour DESC, minute DESC''')
    # We calculate he recent averages to display for better accuracy
    c = 0
    light_avg = 0
    temp_avg = 0
    humidity_avg = 0
    for data in cursor.fetchall():
        light, temp, humidity = data
        light_avg += light
        temp_avg += temp
        humidity_avg += humidity
        c += 1
        if c == 6:
            light_avg /= 6
            temp_avg /= 6
            humidity_avg /= 6
            connection.close()
            return round(temp_avg, 1), round(humidity_avg, 1), round(light_avg, 1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
