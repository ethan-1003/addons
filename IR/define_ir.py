import gpiod
import time

# Cấu hình GPIO
CHIP_NAME = "gpiochip0"  # Tên GPIO chip
LINE_OFFSET = 18         # Chân GPIO (thay đổi tùy theo kết nối)

# Tần số PWM 38kHz
PWM_FREQ = 38000
PWM_PERIOD = 1.0 / PWM_FREQ  # Chu kỳ PWM (giây)
HALF_PERIOD = PWM_PERIOD / 2  # Nửa chu kỳ để tạo duty cycle 50%

# Chuỗi tín hiệu HIGH/LOW đã được định nghĩa trước (giây)
signal_sequence = [
    ("HIGH", 0.009), ("LOW", 0.0045),  # Start bit
    ("HIGH", 0.00056), ("LOW", 0.00056),  # Bit 0
    ("HIGH", 0.00056), ("LOW", 0.00169),  # Bit 1
    ("HIGH", 0.00056), ("LOW", 0.00056),  # Bit 0
    ("HIGH", 0.00056), ("LOW", 0.00169),  # Bit 1
    ("HIGH", 0.00056), ("LOW", 0.0045)   # Stop bit
]

def generate_pwm_38khz(line, duration):
    """
    Tạo xung PWM 38kHz bằng cách bật/tắt GPIO trong khoảng thời gian duration.
    :param line: Đối tượng GPIO line từ libgpiod.
    :param duration: Thời gian chạy PWM (giây).
    """
    end_time = time.time() + duration
    while time.time() < end_time:
        line.set_value(1)  # Bật GPIO
        time.sleep(HALF_PERIOD)  # Giữ nửa chu kỳ
        line.set_value(0)  # Tắt GPIO
        time.sleep(HALF_PERIOD)  # Giữ nửa chu kỳ

def send_ir_signal(chip_name, line_offset, sequence):
    """
    Phát tín hiệu IR theo chuỗi HIGH/LOW sử dụng libgpiod.
    :param chip_name: Tên GPIO chip.
    :param line_offset: Line GPIO cần điều khiển.
    :param sequence: Danh sách [(trạng thái, thời gian), ...].
    """
    chip = gpiod.Chip(chip_name)
    line = chip.get_line(line_offset)

    # Cấu hình GPIO làm đầu ra
    line.request(consumer="ir_signal", type=gpiod.LINE_REQ_DIR_OUT)

    try:
        print("Bắt đầu phát tín hiệu IR...")
        for state, duration in sequence:
            if state == "HIGH":
                generate_pwm_38khz(line, duration)  # Phát PWM 38kHz
            elif state == "LOW":
                line.set_value(0)  # Tắt GPIO
                time.sleep(duration)  # Giữ trạng thái LOW
        print("Phát tín hiệu IR hoàn tất.")
    except KeyboardInterrupt:
        print("Dừng phát tín hiệu.")
    finally:
        line.set_value(0)  # Đảm bảo GPIO tắt
        line.release()
        print("Giải phóng GPIO.")

if __name__ == "__main__":
    # Phát tín hiệu IR
    CHIP_NAME = "gpiochip0"  # Đổi tên chip phù hợp với hệ thống của bạn
    LINE_OFFSET = 18         # Đổi thành chân GPIO kết nối với LED IR

    send_ir_signal(CHIP_NAME, LINE_OFFSET, signal_sequence)

