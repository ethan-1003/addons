import serial
import time

# Cấu hình cổng UART
SERIAL_PORT = '/dev/ttyS0'  # Cổng UART0 trên Orange Pi
BAUDRATE = 9600

def send_and_wait(ser, command, expected_response, timeout=5):
    """
    Gửi lệnh qua RS485 và chờ phản hồi từ ESP32.

    :param ser: Đối tượng serial đã mở
    :param command: Chuỗi tín hiệu cần gửi
    :param expected_response: Chuỗi phản hồi mong đợi
    :param timeout: Thời gian chờ phản hồi (giây)
    :return: True nếu nhận được phản hồi đúng, False nếu timeout
    """
    while True:
        # Gửi lệnh qua RS485
        ser.write(command.encode('utf-8'))
        print(f"Sent: {command.strip()}")

        # Chờ phản hồi
        start_time = time.time()  # Bắt đầu tính thời gian
        while time.time() - start_time < timeout:
            if ser.in_waiting > 0:  # Nếu có dữ liệu trong buffer
                response = ser.readline().decode('utf-8').strip()
                print(f"Received: {response}")
                if response == expected_response:  # Kiểm tra phản hồi đúng
                    return True
        print("No valid response, resending...")  # Nếu không nhận được phản hồi đúng, gửi lại lệnh

try:
    # Mở cổng serial
    ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=1)
    print(f"Connected to {SERIAL_PORT} at {BAUDRATE} baudrate.")

    while True:
        # Bật LED ESP1
        send_and_wait(ser, "1:LED_ON\n", "1:ACK_LED_ON")
        time.sleep(2)

        # Bật LED ESP2
        send_and_wait(ser, "2:LED_ON\n", "2:ACK_LED_ON")
        time.sleep(2)

        # Tắt LED ESP1
        send_and_wait(ser, "1:LED_OFF\n", "1:ACK_LED_OFF")
        time.sleep(2)

        # Tắt LED ESP2
        send_and_wait(ser, "2:LED_OFF\n", "2:ACK_LED_OFF")
        time.sleep(2)

except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")

