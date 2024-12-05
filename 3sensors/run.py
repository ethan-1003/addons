import time
from Adafruit_BMP.BMP085 import BMP085
from DFRobot_Oxygen import DFRobot_Oxygen_IIC
import smbus2
import json
import requests
SHT31_ADDRESS = 0x44
READ_TEMP_HUM_CMD = [0x2C, 0x06]
bus = smbus2.SMBus(5)
bmp180 = BMP085(busnum=5)
def read_sht31():
    try:
        bus.write_i2c_block_data(SHT31_ADDRESS, READ_TEMP_HUM_CMD[0], READ_TEMP_HUM_CMD[1:])
        time.sleep(0.5)
        data = bus.read_i2c_block_data(SHT31_ADDRESS, 0x00, 6)
        temp_raw = (data[0] << 8) + data[1]
        humidity_raw = (data[3] << 8) + data[4]
        temperature = -45 + (175 * temp_raw / 65535.0)
        humidity = (100 * humidity_raw / 65535.0)
        return temperature, humidity
    except Exception as e:
        print(f"Error reading from SHT31: {e}")
        return None, None
# Cấu hình cảm biến
I2C_BUS = 5  # Bus I2C trên thiết bị của bạn
OXYGEN_SENSOR_ADDR = 0x73  # Địa chỉ mặc định của cảm biến

sensor = DFRobot_Oxygen_IIC(I2C_BUS, OXYGEN_SENSOR_ADDR)
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
TEMP_SENSOR_URL = f"{HA_BASE_URL}/sensor.sht31_temperature"
PRESSURE_SENSOR_URL = f"{HA_BASE_URL}/sensor.bmp180_pressure"
HUMIDITY_SENSOR_URL = f"{HA_BASE_URL}/sensor.sht31_humidity"
OXY_SENSOR_URL = f"{HA_BASE_URL}/sensor.Oxygen_concentration"
def post_to_home_assistant(url, payload):
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()  # Kích hoạt ngoại lệ nếu có lỗi HTTP
        print(f"Data posted to {url}: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Home Assistant: {e}")

# Đọc và in dữ liệu oxy
while True:
    oxygen_concentration = sensor.get_oxygen_data(collect_num=20)
    temperature, humidity = read_sht31()
    pressure = bmp180.read_pressure()

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
    humidity_payload = {
        "state": round(humidity, 2),
        "attributes": {
            "unit_of_measurement": "%",
            "friendly_name": "Humidity",
        },
    }
    post_to_home_assistant(HUMIDITY_SENSOR_URL, humidity_payload)
    oxygen_payload = {
        "state": round(oxygen_concentration, 2),
        "attributes": {
            "unit_of_measurement": "%",
            "friendly_name": "Oxygen",
        },
    }
    post_to_home_assistant(OXY_SENSOR_URL, oxygen_payload)
    print(f"Oxygen concentration: {oxygen_concentration:.2f}%")
    print(f"Temperature: {temperature:.2f} °C")
    print(f"Humidity: {humidity:.2f} %")
    print(f"Pressure: {pressure:.2f} Pa")
    time.sleep(10)
