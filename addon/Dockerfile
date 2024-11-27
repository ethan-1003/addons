FROM python:3.10-slim

# Cài đặt các gói cần thiết
RUN apt-get update && apt-get install -y \
    libgpiod-dev \
    && apt-get clean

# Cài đặt thư viện Python
RUN pip install lgpio flask

# Tạo nhóm gpio với GID cố định và thêm root vào nhóm này
RUN groupadd -g 997 gpio && usermod -a -G gpio root

# Tạo thư mục làm việc
WORKDIR /app

# Copy mã nguồn
COPY run.py .

# Chạy ứng dụng
CMD ["python3", "run.py"]

