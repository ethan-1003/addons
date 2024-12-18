from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Endpoint để gửi tín hiệu IR
@app.route("/send_ir", methods=["POST"])
def send_ir():
    """
    API gửi tín hiệu IR với lệnh từ client.
    """
    data = request.json
    command = data.get("command")

    if not command:
        return jsonify({"status": "error", "message": "No IR command provided"}), 400

    try:
        # Giả lập gửi tín hiệu IR - Thay thế bằng lệnh thực tế để điều khiển IR
        print(f"[INFO] Đang gửi tín hiệu IR: {command}")
        # Ví dụ: Gọi file script gửi IR như send_ir.py
        subprocess.run(["python3", "send_ir.py", command], check=True)
        return jsonify({"status": "success", "message": f"IR command '{command}' sent successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint để học tín hiệu IR
@app.route("/learn_ir", methods=["POST"])
def learn_ir():
    """
    API học tín hiệu IR từ thiết bị điều khiển.
    """
    try:
        print("[INFO] Đang học tín hiệu IR...")
        # Giả lập học tín hiệu IR - thay bằng mã thực tế để học lệnh IR
        learned_command = "NEC:0x12345678"  # Mã giả lập
        print(f"[INFO] Đã học được tín hiệu IR: {learned_command}")
        return jsonify({"status": "success", "command": learned_command}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Endpoint để kiểm tra kết nối
@app.route("/", methods=["GET"])
def index():
    """
    Kiểm tra server còn hoạt động.
    """
    return jsonify({"status": "running", "message": "IR Flask Server is running!"}), 200

if __name__ == "__main__":
    # Chạy Flask server trên cổng 5000
    print("[INFO] Khởi động IR Flask Server trên cổng 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)

