import os
import lgpio
from flask import Flask, request, jsonify

# Lấy cấu hình từ Home Assistant
GPIO_PINS = list(map(int, os.getenv("SUPERVISOR_OPTION_PINS", "17,18").split(',')))
DEFAULT_STATE = os.getenv("SUPERVISOR_OPTION_STATE", "off")

# Khởi tạo GPIO
CHIP = 0
h = lgpio.gpiochip_open(CHIP)
for pin in GPIO_PINS:
    lgpio.gpio_claim_output(h, pin)
    lgpio.gpio_write(h, pin, 1 if DEFAULT_STATE == "on" else 0)

# Khởi tạo Flask app
app = Flask(__name__)

@app.route('/gpio', methods=['POST'])
def control_gpio():
    """
    API để điều khiển GPIO
    Yêu cầu JSON:
    {
        "pins": [17, 18],
        "state": "on"
    }
    """
    data = request.json
    pins = data.get("pins", GPIO_PINS)
    state = data.get("state", DEFAULT_STATE)

    if not isinstance(pins, list) or state not in ["on", "off"]:
        return jsonify({"error": "Invalid data. Provide a list of pins and 'on'/'off' state."}), 400

    try:
        for pin in pins:
            lgpio.gpio_write(h, pin, 1 if state == "on" else 0)
        return jsonify({"message": f"GPIO pins {pins} set to {state}."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gpio', methods=['GET'])
def get_gpio_state():
    """
    API để lấy trạng thái hiện tại của nhiều chân GPIO
    """
    states = {pin: "on" if lgpio.gpio_read(h, pin) else "off" for pin in GPIO_PINS}
    return jsonify(states)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        lgpio.gpiochip_close(h)
