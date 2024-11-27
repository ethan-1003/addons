import smbus
import time
import requests

# Địa chỉ I2C của BMP180
BMP180_I2C_ADDR = 0x77

# URL và Token của Home Assistant
HA_URL = "http://192.168.137.244:8123/api/states/sensor.bmp180_fixed"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI2ODI2ZGIzYjU0NDk0MTg1YTZiNDdhNjA1MDIzNzliYSIsImlhdCI6MTczMjUwMDIxNSwiZXhwIjoyMDQ3ODYwMjE1fQ.P7C4gOtzWOb7RsgectX9cXtf30pQrhoYKbAh2j4CePQ"

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}


class BMP180:
    def __init__(self, address=0x77, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)
        self._load_calibration_data()

    def _load_calibration_data(self):
        self.AC1 = self._read_signed_16bit(0xAA)
        self.AC2 = self._read_signed_16bit(0xAC)
        self.AC3 = self._read_signed_16bit(0xAE)
        self.AC4 = self._read_unsigned_16bit(0xB0)
        self.AC5 = self._read_unsigned_16bit(0xB2)
        self.AC6 = self._read_unsigned_16bit(0xB4)
        self.B1 = self._read_signed_16bit(0xB6)
        self.B2 = self._read_signed_16bit(0xB8)
        self.MB = self._read_signed_16bit(0xBA)
        self.MC = self._read_signed_16bit(0xBC)
        self.MD = self._read_signed_16bit(0xBE)

    def _read_signed_16bit(self, register):
        msb, lsb = self.bus.read_i2c_block_data(self.address, register, 2)
        value = (msb << 8) + lsb
        if value > 32767:
            value -= 65536
        return value

    def _read_unsigned_16bit(self, register):
        msb, lsb = self.bus.read_i2c_block_data(self.address, register, 2)
        return (msb << 8) + lsb

    def _read_raw_temperature(self):
        self.bus.write_byte_data(self.address, 0xF4, 0x2E)
        time.sleep(0.005)
        return self._read_unsigned_16bit(0xF6)

    def _read_raw_pressure(self):
        self.bus.write_byte_data(self.address, 0xF4, 0x34)
        time.sleep(0.005)
        msb, lsb, xlsb = self.bus.read_i2c_block_data(self.address, 0xF6, 3)
        return ((msb << 16) + (lsb << 8) + xlsb) >> 8

    def read_temperature(self):
        UT = self._read_raw_temperature()
        X1 = ((UT - self.AC6) * self.AC5) >> 15
        X2 = (self.MC << 11) // (X1 + self.MD)
        B5 = X1 + X2
        return ((B5 + 8) >> 4) / 10.0

    def read_pressure(self):
        UT = self._read_raw_temperature()
        UP = self._read_raw_pressure()

        # Tính toán áp suất
        X1 = ((UT - self.AC6) * self.AC5) >> 15
        X2 = (self.MC << 11) // (X1 + self.MD)
        B5 = X1 + X2

        B6 = B5 - 4000
        X1 = (self.B2 * (B6 * B6 >> 12)) >> 11
        X2 = (self.AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.AC1 * 4 + X3) << 1) + 2) >> 2
        X1 = (self.AC3 * B6) >> 13
        X2 = (self.B1 * ((B6 * B6) >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> 1)

        if B7 < 0x80000000:
            P = (B7 * 2) // B4
        else:
            P = (B7 // B4) * 2

        X1 = (P >> 8) * (P >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * P) >> 16
        return P + ((X1 + X2 + 3791) >> 4)


# Khởi tạo cảm biến BMP180
bmp = BMP180()

while True:
    temperature = bmp.read_temperature()
    pressure = bmp.read_pressure()

    temperature_payload = {
        "state": round(temperature, 2),
        "attributes": {
            "unit_of_measurement": "°C",
            "friendly_name": "Bmp180 Temperature",
        },
    }
    pressure_payload = {
        "state": round(pressure, 1),
        "attributes": {
            "unit_of_measurement": "hPa",
            "friendly_name": "Bmp180 Pressure",
        },
    }

    try:
        response_temp = requests.post(HA_URL, json=temperature_payload, headers=HEADERS)
        response_temp.raise_for_status()
        print(f"Temperature sent: {temperature:.2f}°C")
    except requests.exceptions.RequestException as e:
        print(f"Error sending temperature: {e}")

    try:
        response_press = requests.post(
            HA_URL.replace("sensor.bmp180_fixed", "sensor.bmp180_pressure"),
            json=pressure_payload,
            headers=HEADERS,
        )
        response_press.raise_for_status()
        print(f"Pressure sent: {pressure:.2f} hPa")
    except requests.exceptions.RequestException as e:
        print(f"Error sending pressure: {e}")
    time.sleep(180)

