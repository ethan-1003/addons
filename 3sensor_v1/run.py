import time
import json
import requests
from Adafruit_BMP.BMP085 import BMP085
from DFRobot_Oxygen import DFRobot_Oxygen_IIC
import smbus2

class SensorManager:
    def __init__(self, options_path="/data/options.json"):
        self.options = self.load_options(options_path)
        self.ha_base_url = self.options.get("api_base_url", "http://default-url")
        self.ha_token = self.options.get("api_token", "default-token")
        self.validate_config()
        self.headers = {
            "Authorization": f"Bearer {self.ha_token}",
            "Content-Type": "application/json",
        }
        self.bus = smbus2.SMBus(5)
        self.bmp180 = BMP085(busnum=5)
        self.sht31_address = 0x44
        self.read_temp_hum_cmd = [0x2C, 0x06]
        self.oxygen_sensor = DFRobot_Oxygen_IIC(5, 0x73)

    def load_options(self, file_path):
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading options: {e}")
            return {}

    def validate_config(self):
        if self.ha_base_url == "http://default-url" or self.ha_token == "default-token":
            print("Error: Missing required configuration in options.json.")
            exit(1)

    def read_sht31(self):
        try:
            self.bus.write_i2c_block_data(self.sht31_address, self.read_temp_hum_cmd[0], self.read_temp_hum_cmd[1:])
            time.sleep(0.5)
            data = self.bus.read_i2c_block_data(self.sht31_address, 0x00, 6)
            temp_raw = (data[0] << 8) + data[1]
            humidity_raw = (data[3] << 8) + data[4]
            temperature = -45 + (175 * temp_raw / 65535.0)
            humidity = (100 * humidity_raw / 65535.0)
            return temperature, humidity
        except Exception as e:
            print(f"Error reading from SHT31: {e}")
            return None, None

    def post_to_home_assistant(self, url, payload):
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            print(f"Data posted to {url}: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Error posting to Home Assistant: {e}")

    def run(self):
        while True:
            oxygen_concentration = self.oxygen_sensor.get_oxygen_data(collect_num=20)
            temperature, humidity = self.read_sht31()
            pressure = self.bmp180.read_pressure()

            sensor_data = [
                {
                    "url": f"{self.ha_base_url}/sensor.sht31_temperature",
                    "payload": {
                        "state": round(temperature, 2),
                        "attributes": {
                            "unit_of_measurement": "°C",
                            "friendly_name": "Temperature",
                        },
                    },
                },
                {
                    "url": f"{self.ha_base_url}/sensor.bmp180_pressure",
                    "payload": {
                        "state": round(pressure / 100, 2),
                        "attributes": {
                            "unit_of_measurement": "Hpa",
                            "friendly_name": "Pressure",
                        },
                    },
                },
                {
                    "url": f"{self.ha_base_url}/sensor.sht31_humidity",
                    "payload": {
                        "state": round(humidity, 2),
                        "attributes": {
                            "unit_of_measurement": "%",
                            "friendly_name": "Humidity",
                        },
                    },
                },
                {
                    "url": f"{self.ha_base_url}/sensor.Oxygen_concentration",
                    "payload": {
                        "state": round(oxygen_concentration, 2),
                        "attributes": {
                            "unit_of_measurement": "%",
                            "friendly_name": "Oxygen",
                        },
                    },
                },
            ]

            for data in sensor_data:
                self.post_to_home_assistant(data["url"], data["payload"])

            print(f"Oxygen concentration: {oxygen_concentration:.2f}%")
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Humidity: {humidity:.2f} %")
            print(f"Pressure: {pressure:.2f} Hpa")
            time.sleep(10)

if __name__ == "__main__":
    sensor_manager = SensorManager()
    sensor_manager.run()

