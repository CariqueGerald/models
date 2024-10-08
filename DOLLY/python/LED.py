from gpiozero import LED
import time

LED_PIN = 17
led = LED(LED_PIN)

try:
    print("Turning on LED")
    led.on()
    time.sleep(5)
    print("Turning off LED")
    led.off()
finally:
    led.close()
