#Dowload their names through pip
import pyautogui
import keyboard

#Download pyserial through pip
import serial
import serial.tools.list_ports

programRunning = True

# Get a list of active ports
ports = serial.tools.list_ports.comports()

# Print the list of ports and prompt the user to choose one
print("Available ports:")
for i, port in enumerate(ports):
    print(f"{i+1}. {port.device} ({port.description})")
choice = int(input("Choose a port (1-{}): ".format(len(ports))))
print("Press 'ctrl' to terminate")

# Set the serial port based on the user's choice
ser = serial.Serial(ports[choice-1].device, 9600)

while programRunning:
    if ser.in_waiting > 0:  # Check if there is new data available on the serial port
        data = ser.readline().decode().strip()  # Read data from serial port
        print(data)
        if data == 'CLICKED':  # If the input is 1, simulate a left mouse click
            pyautogui.click(button='left')
    if keyboard.is_pressed("ctrl"):
        ser.close
        print("Terminating...")
        break