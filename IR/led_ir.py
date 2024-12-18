import pigpio
import time

LED_PIN = 18  # GPIO kết nối với đèn hồng ngoại

# Kết nối với pigpio daemon
pi = pigpio.pi()
if not pi.connected:
    print("Không thể kết nối với pigpio daemon!")
    exit()

# Bắt đầu PWM với tần số 38 kHz và duty cycle 50%
FREQ = 38000  # 38 kHz
DUTY_CYCLE = 128  # Giá trị từ 0-255 (50% duty cycle là 128)
pi.set_mode(LED_PIN, pigpio.OUTPUT)
pi.hardware_PWM(LED_PIN, FREQ, DUTY_CYCLE * 390)  # Hardware PWM (tỷ lệ phần nghìn)

try:
    while True:
        print("Đèn hồng ngoại BẬT")
        time.sleep(2)

        print("Đèn hồng ngoại TẮT")
        pi.hardware_PWM(LED_PIN, FREQ, 0)  # Tắt đèn
        time.sleep(2)

        pi.hardware_PWM(LED_PIN, FREQ, DUTY_CYCLE * 390)  # Bật lại đèn
except KeyboardInterrupt:
    print("Dừng chương trình")
finally:
    pi.hardware_PWM(LED_PIN, 0, 0)  # Tắt PWM
    pi.stop()
