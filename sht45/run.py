from SHT4x import SHT4x
from time import sleep
# Khởi tạo cảm biến với bus I2C 1 và địa chỉ 0x44
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

def post_to_home_assistant(url, payload):
    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()  # Kích hoạt ngoại lệ nếu có lỗi HTTP
        print(f"Data posted to {url}: {payload}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting to Home Assistant: {e}")
sensor = SHT4x(bus=5, address=0x44, mode="high")

# Cập nhật dữ liệu từ cảm biến
while True:
 sensor.update()
 temperature = sensor.temperature
 humidity = sensor.humidity
# In ra nhiệt độ và độ ẩm
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

    # Chờ 10 giây trước khi đo lại
    time.sleep(10)
