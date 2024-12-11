import os
import time
import requests
from Adafruit_BMP.BMP085 import BMP085

# Supervisor token lấy từ biến môi trường
SUPERVISOR_TOKEN = os.getenv("SUPERVISOR_TOKEN")

if not SUPERVISOR_TOKEN:
    print("Supervisor token is not available. Make sure the add-on is running under Home Assistant Supervisor.")
    exit(1)

# Home Assistant API URL
HASS_API_URL = "http://supervisor/core/api"

# Hàm gửi dữ liệu cảm biến đến Home Assistant
def send_sensor_data(sensor_name, value, unit):
    url = f"{HASS_API_URL}/states/sensor.{sensor_name}"
    headers = {
        "Authorization": f"Bearer {SUPERVISOR_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {
        "state": value,
        "attributes": {
            "unit_of_measurement": unit,
            "friendly_name": sensor_name,
        },
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"Successfully updated sensor {sensor_name}: {value}{unit}")
        else:
            print(f"Failed to update sensor {sensor_name}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending data to Home Assistant: {e}")

# Khởi tạo cảm biến BMP085
sensor = BMP085(busnum=5)

# Vòng lặp chính
try:
    while True:
        # Đọc dữ liệu từ cảm biến
        temperature = sensor.read_temperature()  # Nhiệt độ (°C)
        pressure = sensor.read_pressure()        # Áp suất (Pa)

        print(f"Nhiệt độ: {temperature:.2f} °C")
        print(f"Áp suất: {pressure:.2f} Pa")
        print("-------------------------------")

        # Gửi dữ liệu nhiệt độ và áp suất lên Home Assistant
        send_sensor_data("bmp180_temperature", round(temperature, 2), "°C")
        send_sensor_data("bmp180_pressure", round(pressure, 2), "Pa")

        # Chờ 10 giây
        time.sleep(10)

except KeyboardInterrupt:
    print("Script stopped by user.")

