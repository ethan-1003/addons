import json
import lgpio
import time

# Đường dẫn file cấu hình
CONFIG_PATH = "/data/options.json"

# Hàm đọc file options.json
def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

# Hàm thiết lập GPIO
def setup_gpio(handle, pin, state):
    # Khai báo chân GPIO ở chế độ output
    lgpio.gpio_claim_output(handle, pin)
    # Đặt trạng thái cho chân (on = HIGH, off = LOW)
    lgpio.gpio_write(handle, pin, int(state == "on"))
    print(f"Set pin {pin} to {'HIGH' if state == 'on' else 'LOW'}")

# Hàm chính
def main():
    # Đọc cấu hình từ file options.json
    config = load_config()
    pin = config.get("pin", None)  # Lấy giá trị pin
    state = config.get("state", "off")  # Lấy trạng thái mặc định là "off"

    # Kiểm tra xem pin có được cấu hình không
    if pin is None:
        raise ValueError("No GPIO pin configured!")

    print(f"Configured pin: {pin}, State: {state}")

    # Mở giao diện GPIO
    handle = lgpio.gpiochip_open(0)

    try:
        # Thiết lập GPIO theo cấu hình
        setup_gpio(handle, pin, state)

        # Giữ chương trình chạy
        print("GPIO configured. Running...")
        while True:
            time.sleep(1)  # Giữ chương trình chạy (hoặc thêm logic khác nếu cần)
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        # Đóng giao diện GPIO
        lgpio.gpiochip_close(handle)
        print("GPIO cleanup complete.")

if __name__ == "__main__":
    main()

