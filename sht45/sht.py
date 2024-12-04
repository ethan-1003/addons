import time
import board
import busio
import adafruit_sht31d

# Tạo I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Khởi tạo cảm biến SHT31D
sht31 = adafruit_sht31d.SHT31D(i2c)

while True:
    # Đọc dữ liệu nhiệt độ và độ ẩm
    temperature = sht31.temperature
    humidity = sht31.relative_humidity
    
    print(f"Temperature: {temperature:.2f} °C")
    print(f"Humidity: {humidity:.2f} %")
    
    # Tạm dừng 2 giây trước khi đọc lại
    time.sleep(2)

