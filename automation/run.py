import time
from Adafruit_BMP import BMP085
import Adafruit_GPIO.I2C as I2C
import lgpio
h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h,17)
I2C.require_repeated_start()
sensor = BMP085.BMP085(busnum=1)
while True:
    # Đọc dữ liệu từ cảm biến
    temperature = sensor.read_temperature()  # Nhiệt độ (°C)
    pressure = sensor.read_pressure()        # Áp suất (Pa)
    altitude = sensor.read_altitude()
    print(f"tem: {temperature}")
    if temperature > 27:
    	lgpio.gpio_write(h,17,1)
    else:
    	lgpio.gpio_write(h,17,0)
    time.sleep(5)

