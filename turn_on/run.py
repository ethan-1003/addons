import lgpio

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h,17)
lgpio.gpio_write(h, 17, 1)  # Bật chân GPIO 17  
print("GPIO 17 đã bật!")

