import json
import lgpio
import os
import time

# Đường dẫn file cấu hình
CONFIG_PATH = "/data/options.json"

# Hàm đọc file options.json
def load_config():
    try:
        # Kiểm tra nếu file không tồn tại
        if not os.path.exists(CONFIG_PATH):
            raise FileNotFoundError(f"Configuration file {CONFIG_PATH} not found.")

        # Kiểm tra nếu file rỗng
        if os.path.getsize(CONFIG_PATH) == 0:
            raise ValueError(f"Configuration file {CONFIG_PATH} is empty.")

        # Đọc file JSON
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in configuration file {CONFIG_PATH}: {e}")

# Hàm thiết lập GPIO
def setup_gpio(handle, pin, state):
    lgpio.gpio_claim_output(handle, pin)
    lgpio.gpio_write(handle, pin, int(state == "on"))
    print(f"Set pin {pin} to {'HIGH' if state == 'on' else 'LOW'}")

# Hàm chính
def main():
    # Đọc cấu hình từ file options.json
    config = load_config()
    pin = config.get("pin", None)
    state = config.get("state", "off")

    if pin is None:
        raise ValueError("No GPIO pin configured!")

    print(f"Configured pin: {pin}, State: {state}")

    # Mở giao diện GPIO
    handle = lgpio.gpiochip_open(0)

    try:
        # Thiết lập GPIO
        setup_gpio(handle, pin, state)
        print("GPIO configured. Running...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting program...")
    finally:
        lgpio.gpiochip_close(handle)
        print("GPIO cleanup complete.")

if __name__ == "__main__":
    main()

