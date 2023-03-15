#Dowload their names through pip
import pyautogui
import keyboard
import time
#Download pyserial through pip
import serial
import serial.tools.list_ports

programRunning = True

screenSizeX = 1920
screenSizeY = 1080

newPercent = 0.0

positiveSideX = screenSizeX/2

# Get a list of active ports
ports = serial.tools.list_ports.comports()

# Print the list of ports and prompt the user to choose one
print("Available ports:")
for i, port in enumerate(ports):
    print(f"{i+1}. {port.device} ({port.description})")
choice = int(input("Choose a port (1-{}): ".format(len(ports))))
print("Press 'ctrl' to terminate")

# Set the serial port based on the user's choice
ser = serial.Serial(ports[choice-1].device, 38400)

while programRunning:
    if ser.in_waiting > 0:  # Check if there is new data available on the serial port
        data = ser.readline().decode().strip()  # Read data from serial port
        #print(data)
        abs(float(data))
        newPercent = float(data) * 0.01
        y = "{:.3f}".format(newPercent)
        
        mousePosX = positiveSideX * float(y)
        print(data)
        print(newPercent)
        print(mousePosX)
        #pyautogui.moveTo(screenSizeX, screenSizeY/2)  # moves mouse to X of 100, Y of 200.
        pyautogui.moveTo(abs(mousePosX), screenSizeY/2)  # moves mouse to X of 100, Y of 200.
        time.sleep(1)
        if data == 'LEFT':  # If the input is LEFT, simulate a left mouse click
            pyautogui.click(button='left')
        if data == 'RIGHT':  # If the input is RIGHT, simulate a right mouse click
            pyautogui.click(button='left')
    if keyboard.is_pressed("ctrl"):
        ser.close
        print("Terminating...")
        break