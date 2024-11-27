FROM python:3.10-slim

# Cài đặt các gói cần thiết cho GPIO
RUN apt-get update && apt-get install -y \
    libgpiod-dev \
    && apt-get clean

# Cài đặt thư viện lgpio và Flask
RUN pip install lgpio flask

# Tạo thư mục làm việc
WORKDIR /app

# Copy mã test GPIO vào container
COPY run.py /app/run.py

# Chạy ứng dụng
CMD ["python3", "run.py"]

