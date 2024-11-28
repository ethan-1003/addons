import lgpio
from time import sleep

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h,17)
lgpio.gpio_write(h,17,0)
print("GPIO 17 da tat")

