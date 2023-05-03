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

newPercentX = 0.0
newPercentY = 0.0

positiveSideX = screenSizeX/2
positiveSideY = screenSizeY/2

interval = 1

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

pyautogui.FAILSAFE = False
pyautogui.PAUSE = False

def add_value_to_rolling_array_x(value):
    rolling_array_x.append(value)
    if len(rolling_array_x) > 5:
        rolling_array_x.pop(0)

def get_rolling_array_average_x():
    if len(rolling_array_x) == 0:
        return None
    else:
        return sum(rolling_array_x) / len(rolling_array_x)

def add_value_to_rolling_array_y(value):
    rolling_array_y.append(value)
    if len(rolling_array_y) > 5:
        rolling_array_y.pop(0)

def get_rolling_array_average_y():
    if len(rolling_array_y) == 0:
        return None
    else:
        return sum(rolling_array_y) / len(rolling_array_y)
    
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

        
        
        add_value_to_rolling_array_x(mousePosX)

        average_x = get_rolling_array_average_x()
        print(average_x)

        add_value_to_rolling_array_y(mousePosY)

        average_y = get_rolling_array_average_y()
        print(average_y)

        lock_time = 0  # Initialize the lock time to 0

        if input1 != prev_input1:
            if input1 == 1:
                if time.time() - lock_time > 0.75:
                    pyautogui.click(button='left')
                    lock_time = time.time()
            elif input1 == 3:
                if time.time() - lock_time > 0.75:
                    pyautogui.doubleClick()
                    lock_time = time.time()

        if input2 != prev_input2:
            if input2 == 2:
                if time.time() - lock_time > 0.75:
                    pyautogui.click(button='right')
                    lock_time = time.time()

        if input3 != prev_input3:
            # Handle input 3 here
            pass

        prev_input1 = input1
        prev_input2 = input2
        prev_input3 = input3



    if keyboard.is_pressed("ctrl"):
        ser.close
        print("Terminating...")
        break