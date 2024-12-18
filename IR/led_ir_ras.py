import gpiod
import time

# Chip và line cho GPIO1_C6
CHIP_NAME = "gpiochip0"  # gpiochip0 chứa GPIO1_C6
LINE_OFFSET = 18         # GPIO1_C6 = line 18 trong gpiochip0

def pwm_generate(chip_name, line_offset, frequency, duty_cycle):
    """
    Tạo tín hiệu PWM liên tục bằng libgpiod 1.x.
    :param chip_name: Tên chip GPIO (gpiochip0, gpiochip1, ...)
    :param line_offset: Line GPIO cần băm xung.
    :param frequency: Tần số PWM (Hz).
    :param duty_cycle: Độ rộng xung (%).
    """
    # Tính toán thời gian bật/tắt
    period = 1.0 / frequency  # Chu kỳ PWM (giây)
    on_time = period * (duty_cycle / 100)  # Thời gian bật
    off_time = period - on_time  # Thời gian tắt

    # Mở chip GPIO và yêu cầu line
    chip = gpiod.Chip(chip_name)
    line = chip.get_line(line_offset)

    # Cấu hình line làm đầu ra
    line.request(consumer="pwm_test", type=gpiod.LINE_REQ_DIR_OUT)

    try:
        print(f"Tạo xung liên tục ở tần số {frequency} Hz với duty cycle {duty_cycle}%...")
        while True:  # Tạo xung liên tục cho đến khi dừng bằng Ctrl+C
            # Bật GPIO
            line.set_value(1)
            time.sleep(on_time)
            # Tắt GPIO
            line.set_value(0)
            time.sleep(off_time)
    except KeyboardInterrupt:
        print("Dừng tạo xung.")
    finally:
        # Giải phóng line
        line.release()
        print("Hoàn tất.")

# Cấu hình PWM
FREQUENCY = 38000       # Tần số 38 kHz
DUTY_CYCLE = 50         # Duty cycle 50% (tần suất bật/tắt cân bằng)

# Tạo xung PWM
pwm_generate(CHIP_NAME, LINE_OFFSET, FREQUENCY, DUTY_CYCLE)

