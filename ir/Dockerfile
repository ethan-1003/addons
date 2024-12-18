# Sử dụng image cơ bản
FROM debian:bullseye

# Cập nhật và cài đặt libgpiod, Python, và các công cụ cần thiết
RUN apt-get update && apt-get install -y \
    libgpiod2 \
    gpiod \
    python3 \
    python3-pip \
    python3-libgpiod \
    && apt-get clean

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy mã Python vào container
COPY . /app

# Chạy script Python (nếu có)
CMD ["python3", "test_lgpiod_ir.py"]

