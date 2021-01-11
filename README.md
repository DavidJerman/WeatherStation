# WeatherStation
A small project, a weather station that displays data on a website.

## Materials required for the project
* Some wood and nails for the weather station
* Humidity and temperature sensor (DHT22)
* Light resistor
* Some LEDs
* Arduino
* Raspberry Pi + Camera
* Jumper wires and 220 Ohm resistors
* Water level sensor (optional)

## How does everything work
Arduino is used to measure the data (temperature, humidity, brightness, water level). The arduino sends its reading over to raspberry pi over a USB cable.
Raspberry pi is responsible for collecting this data and saving it to the sqlite database.
Raspberry pi is also responsible for taking images of the local area with the included camera.
Both data and the images are then displayed on a website. 
Data and image are periodically updated, though the website does not update data dynamically. 
I used Flask to make the website, with a simple html layout.
