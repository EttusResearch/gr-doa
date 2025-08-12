#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
import time

# Configuration
PORT = "/dev/ttyACM0"       # Adapt the Port to your micro:bit
BAUDRATE = 115200   # Must match micro:bit
SERVO_ID = 'A'      # Identifier for the servo
DELAY = 0.1         # Time between updates in seconds

def main():
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        print(f"Connected to {PORT} at {BAUDRATE} baud.")
    except Exception as e:
        print(f"Error opening port: {e}")
        return

    angle = 0
    direction = 1

    try:
        while True:
            angle = max(0, min(180, angle))
            data = f"{SERVO_ID}_{angle}\n"
            ser.write(data.encode('utf-8'))
            print(f"Sent: {data.strip()}")

            angle += direction
            if angle >= 180 or angle <= 0:
                direction *= -1
            time.sleep(DELAY)

    except KeyboardInterrupt:
        print("Stopped by user.")
    finally:
        ser.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()
