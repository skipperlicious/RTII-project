#Dowload their names through pip
import pyautogui
import keyboard

#Download pyserial through pip
import serial
import serial.tools.list_ports
import time

programRunning = True

screenSizeX = 1920
screenSizeY = 1080

newPercent = 0.0

positiveSideX = screenSizeX/2

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

rolling_array = []

def add_value_to_rolling_array(value):
    rolling_array.append(value)
    if len(rolling_array) > 5:
        rolling_array.pop(0)

def get_rolling_array_average():
    if len(rolling_array) == 0:
        return None
    else:
        return sum(rolling_array) / len(rolling_array)

while programRunning:
    if ser.in_waiting > 0:  # Check if there is new data available on the serial port
        data = ser.readline().decode().strip()  # Read data from serial port
        print(data)

        abs(float(data))
        newPercent = float(data) * 0.01
        y = "{:.3f}".format(newPercent)
        
        mousePosX = positiveSideX * float(y)
        print(data)
        print(newPercent)
        print(mousePosX)
        print('END')
        print('\n')
        #pyautogui.moveTo(screenSizeX, screenSizeY/2)  # moves mouse to X of 100, Y of 200.
        pyautogui.moveRel(mousePosX, 0)  # moves mouse to X of 100, Y of 200.

        add_value_to_rolling_array(mousePosX)

        average = get_rolling_array_average()
        print(average)

        if data == '1':  # If the input is 1, simulate a left mouse click
            pyautogui.click()
        if data == '2':  # If the input is 3, simulate a right mouse click
            pyautogui.click(button='right')
        if data == '3':  # If the input is 2, simulate a double left-click
            pyautogui.doubleClick()
    if keyboard.is_pressed("ctrl"):
        ser.close
        print("Terminating...")
        break
