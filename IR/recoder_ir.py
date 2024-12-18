import time
import os

# Đường dẫn sysfs PWM cho pwmchip0 và pwm0 (GPIO18)
PWM_CHIP_PATH = "/sys/class/pwm/pwmchip0"
PWM_CHANNEL_PATH = f"{PWM_CHIP_PATH}/pwm0"

# Tần số và duty cycle cho sóng mang 38kHz
FREQ = 38000  # 38kHz
PERIOD_NS = int(1e9 / FREQ)  # Chu kỳ PWM tính bằng nano giây
DUTY_CYCLE_NS = PERIOD_NS // 2  # Duty cycle 50%

# Danh sách thời gian HIGH và LOW (đơn vị giây)
signal_times = [
    ("HIGH", 0.179723), ("LOW", 0.008993),
    ("HIGH", 0.004499), ("LOW", 0.000596),
    ("HIGH", 0.000533), ("LOW", 0.000615),
    ("HIGH", 0.001626), ("LOW", 0.000592),
    ("HIGH", 0.001674), ("LOW", 0.000574),
    ("HIGH", 0.041228), ("LOW", 0.008992),
]

def write_sysfs(path, value):
    """Hàm ghi giá trị vào file sysfs."""
    with open(path, "w") as f:
        f.write(str(value))

def setup_pwm():
    """Xuất và cấu hình PWM trên GPIO18."""
    if not os.path.exists(PWM_CHANNEL_PATH):
        write_sysfs(f"{PWM_CHIP_PATH}/export", 0)
        time.sleep(0.1)  # Đợi PWM được khởi tạo

    write_sysfs(f"{PWM_CHANNEL_PATH}/period", PERIOD_NS)
    write_sysfs(f"{PWM_CHANNEL_PATH}/duty_cycle", DUTY_CYCLE_NS)

def enable_pwm(enable):
    """Bật hoặc tắt PWM."""
    write_sysfs(f"{PWM_CHANNEL_PATH}/enable", 1 if enable else 0)

def send_ir_signal(times):
    """Gửi tín hiệu IR theo thời gian HIGH và LOW."""
    for state, duration in times:
        if state == "HIGH":
            enable_pwm(True)  # Bật PWM
        elif state == "LOW":
            enable_pwm(False)  # Tắt PWM
        time.sleep(duration)  # Chờ trong khoảng thời gian tương ứng

def cleanup_pwm():
    """Giải phóng PWM sau khi sử dụng."""
    enable_pwm(False)
    write_sysfs(f"{PWM_CHIP_PATH}/unexport", 0)

if __name__ == "__main__":
    try:
        print("Đang khởi tạo PWM...")
        setup_pwm()

        print("Phát lại tín hiệu IR...")
        send_ir_signal(signal_times)
        print("Phát tín hiệu IR hoàn tất.")

    except KeyboardInterrupt:
        print("Dừng chương trình.")
    finally:
        cleanup_pwm()
        print("Đã tắt và giải phóng PWM.")

