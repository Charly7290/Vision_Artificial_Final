import serial
import time

arduino = serial.Serial("COM3", 9600, timeout=1)


def send_servo_command(num):
    msg = f"SERVO:{num}\n"
    arduino.write(msg.encode())
    print("Sent to Arduino:", msg.strip())


def main():
    time.sleep(2)
    send_servo_command(1)  # Run code in Arduino for Servo 1
    time.sleep(2)
    send_servo_command(2)
    time.sleep(2)


if __name__ == "__main__":
    main()
