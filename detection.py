import cv2
import numpy as np
import time
import socket
import json
import threading
from controller import XArm

def activateArm():
    # Print statement
    print("Activating arm...")

    # Activate arm based on object
    if object == 'bottle' or object == 'cup':
        arm.recieve_recycle()
    elif object == 'cardboard' or object == 'garbage_bag':
        arm.recieve_waste()
    elif object == 'apple' or object == 'banana' or object == 'orange':
        arm.recieve_compost()

    print("Pausing for 5 seconds...")
    time.sleep(5)
    print("Back to detecting...")

    return

# Load YOLO model
net = cv2.dnn.readNet("models/yolov3-tiny.weights", "models/yolov3-tiny.cfg")

# Load COCO names 
classes = []
with open("models/coco.names", "r") as f:
    classes = [line.strip() for line in f]

# Set the target classes
target_classes = ['bottle', 'apple', 'cup', 'orange', 'banana']

# Establish connection with arm
arm = XArm()

# Connect to camera
cap = cv2.VideoCapture(0)
width = 320
height = 240
cap.set(3, 320)
cap.set(4, 240)
cap.set(cv2.CAP_PROP_FPS, 1) # 1 frame per second
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 1 frame buffer

# Measure the frames and buffer flag
frameCount = 0
get_rid_of_buffer = False

try:
    while True:

        #client, addr = piSocket.accept()
        #with client:
        #    handleSocket(client)

        # Get the frame
        ret, frame = cap.read()
        if not ret:
            print("Can't get the frame")
            break

        frameCount += 1
        print(f"Detecting Frame #{frameCount}")

        # Get the height and width of the frame
        height, width, _ = frame.shape

        # Preprocess the frame for YOLO
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(net.getUnconnectedOutLayersNames())

        found_detection = False

        # Process each detection
        found_target = False  # Flag variable to indicate if target is found
        for out in outs:
            if found_target:  # If target is already found, break out of the outer loop
                break
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.1 and classes1[class_id] in target_classes:
                    
                    # Object detected
                    object = classes1[class_id]
                    print(f"{object} detected with confidence {confidence}")

                    # Draw bounding box
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    
                    # Get x and y coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    # Draw rectangle around object
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Adjust coordinates to have (0,0) at the center of the frame
                    xcoordinate = x - (width // 2)
                    ycoordinate = (height // 2) - y
                    objectCoordinates = {'x': xcoordinate, 'y': ycoordinate}
                    text = f"x: {objectCoordinates['x']}, y: {objectCoordinates['y']}"
                    print(objectCoordinates)

                    # Define the font scale and thickness
                    font_scale = 1
                    thickness = 2

                    # Calculate text size to determine text width and height
                    text_width, text_height = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)[0]

                    # Calculate the coordinates for placing the text centered and at the bottom
                    text_x = (width - text_width) // 2
                    text_y = height - 10  # You can adjust the value according to your preference

                    # Place coordinates on the frame
                    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale , (0, 255, 0), thickness)



                    # Save image
                    print("Saving frame...")
                    image_filename = f"pictures/{object}_frame{frameCount}.png"
                    cv2.imwrite(image_filename, frame)

                    activateArm()
                
                    # get rid of the buffer
                    _, frame = cap.read()

                    # Set flag to True since target is found
                    found_target = True
                    break  # Break out of the inner loop


        # Save the frame to the "pictures" folder
        #image_filename = f"pictures/frame{frameCount}.png"
        #cv2.imwrite(image_filename, frame)
except KeyboardInterrupt:
    print("KeyboardInterrupt: Stopping the program.")
    cap.release()  # Release the capture device
    cv2.destroyAllWindows()  # Close OpenCV windows

