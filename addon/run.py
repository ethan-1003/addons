import lgpio

h = lgpio.gpiochip_open(0)  # Mở GPIO chip 0
lgpio.gpio_claim_output(h, 17)  # Đặt chân GPIO 17 làm output
lgpio.gpio_write(h, 17, 1)  # Bật chân GPIO 17
lgpio.gpiochip_close(h)  # Đóng chip
print("GPIO 17 đã bật!")
