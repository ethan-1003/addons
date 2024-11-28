import time
from Adafruit_BMP import BMP085
import Adafruit_GPIO.I2C as I2C
import requests

# Chỉ định bus I2C
I2C.require_repeated_start()
sensor = BMP085.BMP085(busnum=1)
HA_URL = "http://192.168.137.244:8123/api/states/sensor.bmp180_temperature"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2ODI2ZGIzYjU0NDk0MTg1YTZiNDdhNjA1MDIzNzliYSIsImlhdCI6MTczMjUwMDIxNSwiZXhwIjoyMDQ3ODYwMjE1fQ.P7C4gOtzWOb7RsgectX9cXtf30pQrhoYKbAh2j4CePQ"

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}
while True:
    temperature = sensor.read_temperature()  # Nhiệt độ (°C)
    pressure = sensor.read_pressure()        # Áp suất (Pa)
    altitude = sensor.read_altitude()        # Độ cao (m)
    temperature_payload = {
                "state": round(temperature, 2),
                "attributes": {
                    "unit_of_measurement": "°C",
                    "friendly_name": "Temperature",
                },
            }
    requests.post(HA_URL, json=temperature_payload, headers=HEADERS)
    print(f"nhiệt độ: {temperature:.2f} °C")
    pressure_payload = {
                "state": round(pressure, 2),
                "attributes": {
                    "unit_of_measurement": "Pa",
                    "friendly_name": "pressure",
                },
            }
    requests.post(HA_URL.replace("sensor.bmp180_temperature","sensor.bmp180_pressure"), json=pressure_payload, headers=HEADERS)
    print(f"Áp suất: {pressure:.2f} Pa")
    altitude_payload = {
                "state": round(altitude, 2),
                "attributes": {
                    "unit_of_measurement": "m",
                    "friendly_name": "altitude",
                },
            }
    requests.post(HA_URL.replace("sensor.bmp180_pressure","sensor.bmp180_altitude"), json=altitude_payload, headers=HEADERS)
    print(f"Độ cao: {altitude:.2f} m")
    time.sleep(10)
