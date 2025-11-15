import serial
import time

arduino = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)

def send_servo_command(num):
    msg = f"SERVO:{num}\n"
    arduino.write(msg.encode())
    print("Sent to Arduino:", msg.strip())

# TEST
send_servo_command(1) #Run code in Arduino for Servo 1
time.sleep(2)
send_servo_command(2)
time.sleep(2)