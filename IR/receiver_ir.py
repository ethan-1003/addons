import pigpio
import time

IR_PIN = 17  # Chân GPIO kết nối với OUT của TI1838
FREQ = 38000

# Kết nối với pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Không thể kết nối pigpio!")
    exit()

# Bộ lưu trữ tín hiệu
data = []

def callback(gpio, level, tick):
    """Hàm callback ghi lại thời gian thay đổi mức tín hiệu."""
    global data
    if level == pigpio.TIMEOUT:
        pi.set_watchdog(IR_PIN, 0)  # Dừng watchdog sau khi hết tín hiệu
        print("Dữ liệu tín hiệu:", data)
    else:
        data.append((tick, level))

# Đặt callback cho chân IR
cb = pi.callback(IR_PIN, pigpio.EITHER_EDGE, callback)

print("Nhấn nút trên remote Funiki...")
pi.set_watchdog(IR_PIN, 50)  # Kích hoạt watchdog 50ms để phát hiện tín hiệu kết thúc

try:
    time.sleep(20)  # Chờ tối đa 10 giây để ghi tín hiệu
except KeyboardInterrupt:
    print("Dừng chương trình")
finally:
    cb.cancel()
    pi.stop()
