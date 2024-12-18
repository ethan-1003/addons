from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template cho giao diện web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Flask Server</title>
    <style>
        body { text-align: center; margin-top: 50px; font-family: Arial, sans-serif; }
        button { padding: 15px 25px; font-size: 18px; cursor: pointer; background-color: #28a745; color: white; border: none; border-radius: 5px; }
        button:hover { background-color: #218838; }
    </style>
</head>
<body>
    <h1>Simple Web Server</h1>
    <p>Nhấn nút bên dưới để gửi yêu cầu tới server.</p>
    <form method="POST" action="/">
        <button type="submit">Nhấn vào đây</button>
    </form>
</body>
</html>
"""

# Route chính: Hiển thị giao diện và xử lý nút nhấn
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        print("Đã nhấn nút trên giao diện web!")  # In ra terminal
    return render_template_string(HTML_TEMPLATE)  # Hiển thị giao diện

# Khởi chạy server Flask
if __name__ == "__main__":
    print("Server đang chạy tại: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

