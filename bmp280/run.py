from bmp280_driver import BMP280
import smbus2  # Thư viện giao tiếp I2C

# Khởi tạo I2C bus
i2c_bus = smbus2.SMBus(5)

# Địa chỉ I2C của BMP280 (thường là 0x76 hoặc 0x77)
bmp280 = BMP280(i2c_addr=0x76, i2c_dev=i2c_bus)

# Thiết lập cảm biến
bmp280.setup(
    mode="normal",                   # Chế độ hoạt động: normal, sleep, forced
    temperature_oversampling=16,     # Hệ số lấy mẫu nhiệt độ
    pressure_oversampling=16,        # Hệ số lấy mẫu áp suất
    temperature_standby=500          # Thời gian chờ giữa các phép đo (ms)
)

# Đọc và in dữ liệu
temperature = bmp280.get_temperature()
pressure = bmp280.get_pressure()
altitude = bmp280.get_altitude(qnh=1013.25)  # Áp suất chuẩn mực nước biển (hPa)

print(f"Nhiệt độ: {temperature:.2f} °C")
print(f"Áp suất: {pressure:.2f} hPa")
print(f"Độ cao: {altitude:.2f} m")
