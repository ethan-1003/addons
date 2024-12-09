FROM python:3.10-slim

# Cài đặt các công cụ cần thiết cho việc biên dịch và xử lý GPIO
RUN apt update && apt install -y \
    python3-dev \
    build-essential \
    gcc \
    libgpiod-dev

# Cài đặt các thư viện Python cần thiết
RUN pip install --no-cache-dir \
    adafruit-circuitpython-dht \
    adafruit-blinka \
    RPi.GPIO \
    smbus2 \
    requests
# Sao chép mã ứng dụng vào container
COPY run.py /run.py
COPY SHT4x.py /SHT4x.py
# Chạy script Python
CMD ["python", "/run.py"]
