#Imported libraries
import pyautogui
import keyboard
import time
import cv2
import dlib
import math
import serial
import serial.tools.list_ports
import threading

arduinoRunning = True
imgprocessingRunning = True

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

pyautogui.FAILSAFE = False
pyautogui.PAUSE = False

def midpoint(point1 ,point2):
    return (point1.x + point2.x)/2,(point1.y + point2.y)/2

def euclidean_distance(point1 , point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_blink_ratio(eye_points, facial_landmarks):
    
    #loading all the required points
    corner_left  = (facial_landmarks.part(eye_points[0]).x, 
                    facial_landmarks.part(eye_points[0]).y)
    corner_right = (facial_landmarks.part(eye_points[3]).x, 
                    facial_landmarks.part(eye_points[3]).y)
    
    center_top    = midpoint(facial_landmarks.part(eye_points[1]), 
                             facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), 
                             facial_landmarks.part(eye_points[4]))

    #calculating distance
    horizontal_length = euclidean_distance(corner_left,corner_right)
    vertical_length = euclidean_distance(center_top,center_bottom)

    ratio = horizontal_length / vertical_length

    return ratio

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

#livestream from the webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#in case of a video:
#cap = cv2.VideoCapture("__path_of_the_video__")

#name of the display window in openCV
cv2.namedWindow('BlinkDetector')

#Init dlib front face detector
detector = dlib.get_frontal_face_detector()

#init dlib predictor
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

#these landmarks are based on the image above 
left_eye_landmarks  = [36, 37, 38, 39, 40, 41]
right_eye_landmarks = [42, 43, 44, 45, 46, 47]

def arduino_loop():
    while arduinoRunning:
        if ser.in_waiting > 0:  # Check if there is new data available on the serial port
            data = ser.readline().decode().strip()  # Read data from serial port
            input1, input2, input3, input4 = data.split(",")
            #print(input1, input2, input3, input4)

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
            #print(average_x)

            add_value_to_rolling_array_y(mousePosY)

            average_y = get_rolling_array_average_y()
            #print(average_y)

            if keyboard.is_pressed("ctrl"):
                ser.close
                cap.release()
                cv2.destroyAllWindows()
                print("Terminating...")
                break

def blink_detector_loop():

    #variables

    BLINK_RATIO_THRESHOLD = 6

    blink_counter = 0
    blink_counter_2 = 0

    left_eye_closed = False
    right_eye_closed = False

    left_mouse_button_pressed = False
    right_mouse_button_pressed = False

    hold_duration = 0.5

    while True:
        #capturing frame
        retval, frame = cap.read()

        #exit the application if frame not found
        if not retval:
            print("Can't receive frame (stream end?). Exiting ...")
            break 

        #converting image to grayscale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Face detection with dlib
        #detecting faces in the frame 
        faces,_,_ = detector.run(image = frame, upsample_num_times = 0, adjust_threshold = 0.0)

        for face in faces:
        
            landmarks = predictor(frame, face)

            #Calculating blink ratio for one eye
            right_eye_ratio  = get_blink_ratio(left_eye_landmarks, landmarks)
            left_eye_ratio = get_blink_ratio(right_eye_landmarks, landmarks)
            blink_ratio     = (left_eye_ratio + right_eye_ratio) / 2
        
        if left_eye_ratio > BLINK_RATIO_THRESHOLD:
            #Increment the blink counter
            blink_counter += 1

            pyautogui.click()
            print("LEFT clicked")

            # Check if the blink counter has reached 10
            if blink_counter >= 10:
                # Eye is closed! Do Something!
                cv2.putText(frame, "LEFT EYE CLOSED", (10,50), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,255,255), 2, cv2.LINE_AA)
                left_eye_closed = True
                if not left_mouse_button_pressed:
                    # Hold down the left mouse button
                    pyautogui.mouseDown(button='left')
                    left_mouse_button_pressed = True
                else:
                    # Check if the mouse button is pressed
                    if left_mouse_button_pressed:
                        # Release the left mouse button
                        pyautogui.mouseUp(button='left')
                        left_mouse_button_pressed = False
                # Reset the blink counter
                blink_counter = 0
        else:
            # Reset the blink counter if the eye is open
            blink_counter_2 = 0
            left_eye_closed = False

        if right_eye_ratio > BLINK_RATIO_THRESHOLD:
            # Increment the blink counter
            blink_counter_2 += 1

            # Check if the blink counter has reached 10
            if blink_counter_2 >= 10:
                # Eye is closed
                cv2.putText(frame, "RIGHT EYE CLOSED", (10,50), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (255,255,255), 2, cv2.LINE_AA)
                pyautogui.click(button='right')
                print("RIGHT clicked")
                right_eye_closed = True
                if not right_mouse_button_pressed:
                    #Hold down the left mouse button
                    pyautogui.mouseDown(button='right')
                    right_mouse_button_pressed = True
                else:
                    #Check if the mouse button is pressed
                    pyautogui.PAUSE = hold_duration
                    if right_mouse_button_pressed:
                        # Release the left mouse button
                        pyautogui.mouseUp(button='right')
                        right_mouse_button_pressed = False
                #Reset the blink counter
                blink_counter_2 = 0
        else:
            #Reset the blink counter if the eye is open
            blink_counter_2 = 0
            right_eye_closed = False

        key = cv2.waitKey(1)
        if key == 27:
            break
    
        if keyboard.is_pressed("ctrl"):
            ser.close
            cap.release()
            cv2.destroyAllWindows()
            print("Terminating...")
            break

# Create and start threads
blink_detector_thread = threading.Thread(target=blink_detector_loop)
blink_detector_thread.start()

# Create and start threads
arduino_thread = threading.Thread(target=arduino_loop)
arduino_thread.start()

# Wait for threads to finish
arduino_thread.join()
blink_detector_thread.join()
