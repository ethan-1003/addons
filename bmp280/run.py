from bmp280 import BMP280
from smbus2 import SMBus
import requests
import time

# Khởi tạo SMBus
bus = SMBus(1)

# Khởi tạo cảm biến BMP280
bmp280 = BMP280(i2c_dev=bus)
HA_BASE_URL = "http://192.168.137.253:8123/api/states"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0ODgyY2UxNmE0YjE0ODEwYTVhMGQzZmFlMzA4OGQ4YyIsImlhdCI6MTczMzE3Nzk4MSwiZXhwIjoyMDQ4NTM3OTgxfQ.5D2N2JFy1JzkHKc7-cR1Eo8eyO4Erke0hZOZqiX1FkE"

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# URL cho từng cảm biến
TEMP_SENSOR_URL = f"{HA_BASE_URL}/sensor.bmp280_temperature"
PRESSURE_SENSOR_URL = f"{HA_BASE_URL}/sensor.bmp280_pressure"

def post_to_home_assistant(url, payload):
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()  # Kích hoạt ngoại lệ nếu có lỗi HTTP
        print(f"Data posted to {url}: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Home Assistant: {e}")

while True:
    temperature = bmp280.get_temperature()
    pressure = bmp280.get_pressure()

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

    # In dữ liệu ra màn hình
    print(f"Nhiệt độ: {temperature:.2f} °C")
    print(f"Áp suất: {pressure:.2f} hPa")
    
    # Thêm thời gian nghỉ giữa các lần đọc dữ liệu
    time.sleep(10)
