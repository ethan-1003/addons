import time
from Adafruit_BMP import BMP085
import Adafruit_GPIO.I2C as I2C
import requests

# Khởi tạo cảm biến BMP180
I2C.require_repeated_start()
sensor = BMP085.BMP085(busnum=1)

# URL API của Home Assistant
HA_BASE_URL = "http://192.168.137.244:8123/api/states"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2ODI2ZGIzYjU0NDk0MTg1YTZiNDdhNjA1MDIzNzliYSIsImlhdCI6MTczMjUwMDIxNSwiZXhwIjoyMDQ3ODYwMjE1fQ.P7C4gOtzWOb7RsgectX9cXtf30pQrhoYKbAh2j4CePQ"

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# URL cho từng cảm biến
TEMP_SENSOR_URL = f"{HA_BASE_URL}/sensor.bmp180_temperature"
PRESSURE_SENSOR_URL = f"{HA_BASE_URL}/sensor.bmp180_pressure"
ALTITUDE_SENSOR_URL = f"{HA_BASE_URL}/sensor.bmp180_altitude"

def post_to_home_assistant(url, payload):
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()  # Kích hoạt ngoại lệ nếu có lỗi HTTP
        print(f"Data posted to {url}: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Home Assistant: {e}")

while True:
    # Đọc dữ liệu từ cảm biến
    temperature = sensor.read_temperature()  # Nhiệt độ (°C)
    pressure = sensor.read_pressure()        # Áp suất (Pa)
    altitude = sensor.read_altitude()        # Độ cao (m)

    # Gửi dữ liệu nhiệt độ
    temperature_payload = {
        "state": round(temperature, 2),
        "attributes": {
            "unit_of_measurement": "°C",
            "friendly_name": "Temperature",
        },
    }
    post_to_home_assistant(TEMP_SENSOR_URL, temperature_payload)

    # Gửi dữ liệu áp suất
    pressure_payload = {
        "state": round(pressure, 2),
        "attributes": {
            "unit_of_measurement": "Pa",
            "friendly_name": "Pressure",
        },
    }
    post_to_home_assistant(PRESSURE_SENSOR_URL, pressure_payload)

    # Gửi dữ liệu độ cao
    altitude_payload = {
        "state": round(altitude, 2),
        "attributes": {
            "unit_of_measurement": "m",
            "friendly_name": "Altitude",
        },
    }
    post_to_home_assistant(ALTITUDE_SENSOR_URL, altitude_payload)

    # In dữ liệu ra màn hình
    print(f"Nhiệt độ: {temperature:.2f} °C")
    print(f"Áp suất: {pressure:.2f} Pa")
    print(f"Độ cao: {altitude:.2f} m")
    print("-------------------------------")

    # Chờ 10 giây trước khi đo lại
    time.sleep(10)

