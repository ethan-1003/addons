import gpiod
import time

# Cấu hình GPIO
CHIP_NAME = "gpiochip0"  # Chip GPIO (kiểm tra bằng gpiodetect)
LINE_OFFSET = 28         # GPIO0_D4 tương ứng với line 28

# Mở chip GPIO
chip = gpiod.Chip(CHIP_NAME)
line = chip.get_line(LINE_OFFSET)

# Cấu hình chân GPIO làm đầu vào
line.request(consumer="ir_sensor", type=gpiod.LINE_REQ_DIR_IN)

try:
    print("Đang ghi tín hiệu IR từ TI1838 (GPIO0_D4)... Nhấn Ctrl+C để dừng.")
    last_state = line.get_value()  # Trạng thái ban đầu của GPIO
    last_change = time.time()  # Thời gian thay đổi trạng thái cuối cùng
    signal_data = []  # Danh sách lưu tín hiệu (trạng thái, thời gian)

    while True:
        current_state = line.get_value()
        current_time = time.time()
        
        if current_state != last_state:  # Phát hiện thay đổi trạng thái
            elapsed_time = current_time - last_change  # Thời gian giữ trạng thái trước
            signal_data.append((last_state, elapsed_time))  # Lưu trạng thái và thời gian
            last_state = current_state  # Cập nhật trạng thái
            last_change = current_time  # Cập nhật thời gian thay đổi

except KeyboardInterrupt:
    print("Dừng ghi tín hiệu IR.")
finally:
    line.release()

    # In tín hiệu đã ghi nhận
    print("\nTín hiệu IR ghi nhận:")
    for state, time_length in signal_data:
        state_str = "LOW" if state == 0 else "HIGH"
        print(f"{state_str} trong {time_length:.6f} giây")

