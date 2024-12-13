import serial

# Cấu hình UART0
SERIAL_PORT = '/dev/ttyS0'
BAUDRATE = 9600

def listen_uart():
    try:
        # Mở cổng UART
        ser = serial.Serial(SERIAL_PORT, baudrate=BAUDRATE, timeout=None)  # timeout=None để chờ không giới hạn
        print(f"Listening on {SERIAL_PORT} at {BAUDRATE} baudrate...")

        while True:
            # Đọc dữ liệu khi nhận được
            data = ser.readline()  # Đọc một dòng (dữ liệu kết thúc bằng ký tự ngắt dòng)
            if data:
                print(f"Received: {data.decode().strip()}")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nExiting program...")
    finally:
        if ser and ser.is_open:
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    listen_uart()

