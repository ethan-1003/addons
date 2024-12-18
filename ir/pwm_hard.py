import time
import os

PWM_CHIP = "pwmchip2"
PWM_CHANNEL = "pwm0"
PWM_PATH = f"/sys/class/pwm/{PWM_CHIP}/{PWM_CHANNEL}"

def configure_pwm(period_ns, duty_cycle_ns):
    """Cấu hình kênh PWM."""
    try:
        # Export channel nếu chưa được export
        if not os.path.exists(PWM_PATH):
            with open(f"/sys/class/pwm/{PWM_CHIP}/export", "w") as f:
                f.write("0")
            time.sleep(0.2)  # Chờ phần cứng khởi tạo

        # Đặt period
        with open(f"{PWM_PATH}/period", "w") as f:
            f.write(str(period_ns))
            f.flush()
        time.sleep(0.1)  # Chờ phần cứng áp dụng

        # Đặt duty_cycle
        with open(f"{PWM_PATH}/duty_cycle", "w") as f:
            f.write(str(duty_cycle_ns))
            f.flush()
        time.sleep(0.1)

        # Bật PWM
        with open(f"{PWM_PATH}/enable", "w") as f:
            f.write("1")
            f.flush()
    except IOError as e:
        raise RuntimeError(f"Lỗi khi cấu hình PWM: {e}")

def disable_pwm():
    """Tắt kênh PWM."""
    try:
        with open(f"{PWM_PATH}/enable", "w") as f:
            f.write("0")
        time.sleep(0.1)  # Chờ tắt
        with open(f"/sys/class/pwm/{PWM_CHIP}/unexport", "w") as f:
            f.write("0")
    except IOError as e:
        print(f"Lỗi khi tắt PWM: {e}")

if __name__ == "__main__":
    # Tần số 38 kHz, độ rộng xung 50%
    period_ns = 26316  # Chu kỳ 38 kHz
    duty_cycle_ns = 13158  # Độ rộng xung 50%

    try:
        print("Cấu hình PWM...")
        configure_pwm(period_ns, duty_cycle_ns)
        print(f"PWM đang chạy với chu kỳ {period_ns} ns và độ rộng xung {duty_cycle_ns} ns.")
        time.sleep(10)  # Chạy PWM trong 10 giây
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        print("Tắt PWM.")
        disable_pwm()
        print("Hoàn tất.")

