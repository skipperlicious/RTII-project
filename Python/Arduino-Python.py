#Dowload their names through pip
import pyautogui
import keyboard
import time
#Download pyserial through pip
import serial
import serial.tools.list_ports
import dataclasses

programRunning = True

screenSizeX = 1920
screenSizeY = 1080

newPercentX = 0.0
newPercentY = 0.0

positiveSideX = screenSizeX/2
positiveSideY = screenSizeY/2

interval = 3

start_time = time.time()

# Get a list of active ports
ports = serial.tools.list_ports.comports()

# Print the list of ports and prompt the user to choose one
print("Available ports:")
for i, port in enumerate(ports):
    print(f"{i+1}. {port.device} ({port.description})")
choice = int(input("Choose a port (1-{}): ".format(len(ports))))
print("Press 'ctrl' to terminate")
pyautogui.moveTo(screenSizeX/2, screenSizeY/2)  # moves mouse to X of 100, Y of 200.

# Set the serial port based on the user's choice
ser = serial.Serial(ports[choice-1].device, 38400)



rolling_array_x = []
rolling_array_y = []
rolling_array_input1 = []
rolling_array_input2 = []
rolling_array_input3 = []

pyautogui.FAILSAFE = False
pyautogui.PAUSE = False

counter = 0
maxCount = 30

    
while programRunning:
    if ser.in_waiting > 0:  # Check if there is new data available on the serial port
        data = ser.readline().decode().strip()  # Read data from serial port
        print(data)
        input1, input2, input3, input4 = data.split(",")
        print(input1, input2, input3, input4)
        abs(float(input3))
        newPercentX = float(input3) * 0.0001
        y = "{:.3f}".format(newPercentX)

        abs(float(input4))
        newPercentY = float(input4) * 0.0001
        y2 = "{:.3f}".format(newPercentY)
        
        mousePosX = positiveSideX * float(y)
        #print(newPercentX)
        #print(mousePosX)

        mousePosY = positiveSideY * float(y2)
        #print(newPercentY)
        #print(mousePosY)
        
        #print('END')
        #print('\n')
        
        #pyautogui.moveTo(screenSizeX, screenSizeY/2, _pause = False)  # moves mouse to X of 100, Y of 200.
        pyautogui.moveRel(mousePosX, 0, _pause = False)  # moves mouse to X of 100, Y of 200.
        pyautogui.moveRel(0, mousePosY, _pause = False)  # moves mouse to X of 100, Y of 200.

        
        
        
        

        lock_time = 0  # Initialize the lock time to 0

        if int(input1) == 1:  # If the input is LEFT, simulate a left mouse click
            if time.time() - lock_time > interval:  # Check if enough time has elapsed since the last output
                pyautogui.click(button='left')
                lock_time = time.time()  # Update the lock time to the current time
        if int(input2) == 2:  # If the input is RIGHT, simulate a right mouse click
            if time.time() - lock_time > interval:  # Check if enough time has elapsed since the last output
                pyautogui.click(button='right')
                lock_time = time.time()  # Update the lock time to the current time
        if int(input1) == 3:  # If the input is RIGHT, simulate a double click
            if time.time() - lock_time > interval:  # Check if enough time has elapsed since the last output
                pyautogui.doubleClick()
                lock_time = time.time()  # Update the lock time to the current time
                delta_time = time.time() - start_time
                if(delta_time <= interval):
                    start_time = time.time()
        
    if keyboard.is_pressed("ctrl"):
        ser.close
        print("Terminating...")
        break