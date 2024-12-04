import smbus2
import time

SHT45_ADDRESS = 0x44  # Địa chỉ của cảm biến SHT45
bus = smbus2.SMBus(1)  # Mở giao tiếp I2C trên bus 1

try:
    # Gửi một lệnh đơn giản tới cảm biến (ví dụ: Ping)
    bus.write_byte(SHT45_ADDRESS, 0x2C)
    print("Cảm biến phản hồi!")
except Exception as e:
    print(f"Lỗi giao tiếp I2C: {e}")

