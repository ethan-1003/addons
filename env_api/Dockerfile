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
    requests
RUN pip install smbus
RUN pip install smbus2
RUN pip install adafruit-bmp
RUN pip install i2cdevice
# Sao chép mã ứng dụng vào container
COPY run.py /run.py
COPY library /library
#COPY options.json /data/options.json
# Chạy script Python
CMD ["python", "/run.py"]
