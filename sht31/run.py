import time
import smbus2
import adafruit_sht31d
import requests
import json

# Hàm đọc cấu hình từ file options.json
def load_options(file_path="/data/options.json"):
    try:
        with open(file_path, "r") as file:
            options = json.load(file)
            return options
    except FileNotFoundError:
        print(f"Error: {file_path} not found!")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return {}

# Tải thông tin cấu hình từ options.json
options = load_options()
HA_BASE_URL = options.get("api_base_url", "http://default-url")
HA_TOKEN = options.get("api_token", "default-token")

# Kiểm tra nếu thiếu cấu hình cần thiết
if HA_BASE_URL == "http://default-url" or HA_TOKEN == "default-token":
    print("Error: Missing required configuration in options.json.")
    exit(1)

# Thiết lập header cho API
HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

# URL cho từng cảm biến
TEMP_SENSOR_URL = f"{HA_BASE_URL}/sensor.sht31_temperature"
HU_SENSOR_URL = f"{HA_BASE_URL}/sensor.sht31_humidity"

# Khởi tạo bus I2C với smbus2
i2c = smbus2.SMBus(1)  # Dùng bus I2C 1 trên Raspberry Pi

# Khởi tạo cảm biến SHT31 với địa chỉ I2C là 0x44
sht31 = adafruit_sht31d.SHT31D(i2c, address=0x44)

# Hàm gửi dữ liệu đến Home Assistant
def post_to_home_assistant(url, payload):
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()  # Kích hoạt ngoại lệ nếu có lỗi HTTP
        print(f"Data posted to {url}: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Home Assistant: {e}")

# Vòng lặp chính
while True:
    # Đọc dữ liệu từ cảm biến
    temperature = sht31.temperature
    humidity = sht31.relative_humidity

    # Gửi dữ liệu nhiệt độ
    temperature_payload = {
        "state": round(temperature, 2),
        "attributes": {
            "unit_of_measurement": "°C",
            "friendly_name": "Temperature",
        },
    }
    post_to_home_assistant(TEMP_SENSOR_URL, temperature_payload)

    # Gửi dữ liệu độ ẩm
    humidity_payload = {
        "state": round(humidity, 2),
        "attributes": {
            "unit_of_measurement": "%",
            "friendly_name": "Humidity",
        },
    }
    post_to_home_assistant(HU_SENSOR_URL, humidity_payload)

    # In dữ liệu ra màn hình
    print(f"Nhiệt độ: {temperature:.2f} °C")
    print(f"Độ ẩm: {humidity:.2f} %")
    print("-------------------------------")

    # Chờ 10 giây trước khi đo lại
    time.sleep(10)

