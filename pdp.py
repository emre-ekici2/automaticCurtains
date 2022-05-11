#import libraries
import RPi.GPIO as GPIO
import time
import datetime

#set GPIO mode
GPIO.setmode(GPIO.BCM)

#declar variable
ldr = 17
closeCurtains = "20:00:00"
openCurtains = "07:00:00"
curtainStatus = 0
control_pins = [25, 24, 7, 8]
halfstep_seq = [
  [1,0,0,0],
  [1,1,0,0],
  [0,1,0,0],
  [0,1,1,0],
  [0,0,1,0],
  [0,0,1,1],
  [0,0,0,1],
  [1,0,0,1]
]

#set GPIO pins
for pin in control_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 1)

GPIO.setup(ldr, GPIO.IN)

#infinite loop
while True:
    #grab current time and print
    currentTime = datetime.datetime.now()
    currentTimeBrussels = currentTime
    timeNow = currentTimeBrussels.strftime("%H:%M:%S")
    print(timeNow)
    
    #check current light situation and print
    if GPIO.input(ldr) == False:
        print("Dark")
    else:
        print("Light")

    #check if curtains are currently open or closed
    if curtainStatus == 0:
        #if curtains are closed and its 8 am or it is light outside, we open them by rotating the motor 180 degrees
        if (timeNow == openCurtains) or ((GPIO.input(ldr) == True)):
            for i in range(256):
                for halfstep in halfstep_seq[::-1]:
                    for pin in range(4):
                        GPIO.output(control_pins[pin], halfstep[pin])
                    time.sleep(0.001)
            curtainStatus = 1
            print("Curtains closed")

    if curtainStatus == 1:
        #if curtains are opened and its 8pm or it is dark outside, we close them by rotating the motor -180 degrees
        if (timeNow == closeCurtains) or ((GPIO.input(ldr) == False)):
            for i in range(256):
                for halfstep in halfstep_seq[::1]:
                    for pin in range(4):
                        GPIO.output(control_pins[pin], halfstep[pin])
                    time.sleep(0.001)
            curtainStatus = 0
            print("Curtains opened")
    time.sleep(.5)

    
