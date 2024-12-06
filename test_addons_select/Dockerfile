FROM python:3.10-slim

# Cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y \
    libgpiod-dev \
    && apt-get clean

# Cài đặt Flask và lgpio

# Copy mã nguồn
WORKDIR /app
COPY run.py .

# Chạy ứng dụng
CMD ["python3", "run.py"]
