import time
from DFRobot_Oxygen import DFRobot_Oxygen_IIC

# Cấu hình cảm biến
I2C_BUS = 5  # Bus I2C trên thiết bị của bạn
OXYGEN_SENSOR_ADDR = 0x73  # Địa chỉ mặc định của cảm biến

sensor = DFRobot_Oxygen_IIC(I2C_BUS, OXYGEN_SENSOR_ADDR)

# Đọc và in dữ liệu oxy
while True:
    oxygen_concentration = sensor.get_oxygen_data(collect_num=20)
    print(f"Nồng độ Oxy: {oxygen_concentration:.2f}%")
    time.sleep(1)
