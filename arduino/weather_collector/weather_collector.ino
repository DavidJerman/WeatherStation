#include "DHT.h"
#include <Wire.h>
#include <Adafruit_BMP085.h>

#define LIGHT_PIN A0
#define WATER_PIN A1
#define AIR_PIN A2
#define LED_ON 3
#define LED_OFF 4
#define RESET 5
#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)

#define seaLevelPressure_hPa 1013.25

Adafruit_BMP085 bmp;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(LIGHT_PIN, INPUT);
  pinMode(WATER_PIN, INPUT);
  pinMode(LED_ON, OUTPUT);
  pinMode(LED_OFF, OUTPUT);
  pinMode(RESET, OUTPUT);
  digitalWrite(LED_ON, 1);
  digitalWrite(LED_OFF, 0);
  digitalWrite(RESET, 0);
  Serial.begin(9600);
  dht.begin();
  // if (!bmp.begin()) {
  //   Serial.println("Could not find a valid BMP085 sensor, check wiring!");
  //   while (1) {}
  // }
}

void loop() {
  delay(200);
  double light_avgs = 0;
  double water_avgs = 0;
  double air_avgs = 0;
  for (int i = 0; i < 20; i++) {
    double light_sum = 0;
    double water_sum = 0;
    double air_sum = 0;
    for (int j = 0; j < 20; j++) {
      light_sum += analogRead(LIGHT_PIN)/1024.0;
      water_sum += analogRead(WATER_PIN)/256.0;
      air_sum += analogRead(AIR_PIN);
      delay(25);
    }
    
    water_avgs += water_sum/20.0;
    light_avgs += light_sum/20.0;
    air_avgs += air_sum/20.0;
  }
  double water_average_lvl = water_avgs/20.0;
  double light_average_lvl = light_avgs/20.0;
  double air_average_lvl = air_avgs/20.0;

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    digitalWrite(LED_ON, 0);
    digitalWrite(LED_OFF, 1);
    delay(2000);
    digitalWrite(RESET, 1);
  }  

  digitalWrite(LED_ON, 1);
  digitalWrite(LED_OFF, 0);
  Serial.print("light:[");
  Serial.print(light_average_lvl);
  Serial.print("],water:[");
  Serial.print(water_average_lvl);
  Serial.print("],temp:[");
  Serial.print(t);
  Serial.print("],humidity:[");
  Serial.print(h);
  Serial.print("],air:[");
  Serial.print(air_average_lvl);
  Serial.println("]");
}
