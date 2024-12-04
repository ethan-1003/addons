import smbus2
import time
import json
import requests

# Đọc cấu hình từ file options.json
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

# Lấy cấu hình từ file
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

# URL cho các cảm biến
TEMP_SENSOR_URL = f"{HA_BASE_URL}/sensor.sht45_temperature"
HU_SENSOR_URL = f"{HA_BASE_URL}/sensor.sht45_humidity"

# Địa chỉ I2C của cảm biến SHT45
SHT45_ADDRESS = 0x44  # Địa chỉ I2C của SHT45
READ_TEMP_HUM_CMD = [0x24, 0x00]  # Lệnh đọc nhiệt độ và độ ẩm

bus = smbus2.SMBus(1)

# Hàm đọc dữ liệu từ cảm biến SHT45
def read_sht45():
    try:
        # Gửi lệnh đọc dữ liệu nhiệt độ và độ ẩm
        bus.write_i2c_block_data(SHT45_ADDRESS, READ_TEMP_HUM_CMD[0], READ_TEMP_HUM_CMD[1:])
        time.sleep(0.5)  # Đợi một chút để cảm biến phản hồi

        # Đọc 6 byte dữ liệu từ cảm biến (2 byte nhiệt độ, 2 byte độ ẩm)
        data = bus.read_i2c_block_data(SHT45_ADDRESS, 0x00, 6)

        # Giải mã nhiệt độ và độ ẩm từ dữ liệu
        temp_raw = (data[0] << 8) + data[1]
        humidity_raw = (data[3] << 8) + data[4]

        # Tính toán nhiệt độ và độ ẩm từ giá trị thô
        temperature = -45 + (175 * temp_raw / 65535.0)
        humidity = (100 * humidity_raw / 65535.0)

        return temperature, humidity
    except Exception as e:
        print(f"Error reading from SHT45: {e}")
        return None, None

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
    # Đọc dữ liệu từ cảm biến SHT45
    temperature, humidity = read_sht45()

    if temperature is not None and humidity is not None:
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
        print(f"Temperature: {temperature:.2f} °C")
        print(f"Humidity: {humidity:.2f} %")
    else:
        print("Failed to read data.")

    # Chờ 5 giây trước khi đo lại
    time.sleep(5)
