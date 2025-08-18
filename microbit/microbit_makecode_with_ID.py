# You have to add the Servo library for the PCA9685 Servo Driver to run this program.
# You find the library at https://github.com/waveshare/pxt-Servo.
# This program has to be run in the makecode environment.

angle = ""
serial.set_baud_rate(BaudRate.BAUD_RATE115200)
Servo.servo(0, 90)
Servo.servo(1, 90)
Servo.servo(2, 90)

def on_forever():
    global angle
    angle = serial.read_until(serial.delimiters(Delimiters.NEW_LINE))
    #serial.write_line(angle)
    parts = angle.split("_")
    if len(parts) == 2:
        if parts[0] == "A":
            Servo.servo(0, parse_float(parts[1]))
            #basic.show_string("" + str(parse_float(parts[1])))
        if parts[0] == "B":
            Servo.servo(1, parse_float(parts[1]))
            #basic.show_string("" + str(parse_float(parts[1])))
        if parts[0] == "C":
            Servo.servo(2, parse_float(parts[1]))
            #basic.show_string("" + str(parse_float(parts[1])))
        
    basic.pause(100)

basic.forever(on_forever)
