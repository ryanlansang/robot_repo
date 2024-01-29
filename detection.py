import cv2
import numpy as np
import time
from controller import XArm

def activateArm(object):
    # Print statements
    print(f"Detected {object}!")
    print("Activating arm...")

    # Save image
    image_filename = f"pictures/{object}_frame{frameCount}.png"
    cv2.imwrite(image_filename, frame)

    # Activate arm based on object
    if object == 'bottle' or object == 'cup':
        arm.recieve_recycle()
    elif object == 'cardboard' or object == 'garbage_bag':
        arm.recieve_waste()
    elif object == 'apple' or object == 'banana' or object == 'orange':
        arm.recieve_compost()

    print("Back to detecting...")

# Load YOLO model
net = cv2.dnn.readNet("models/yolov3-tiny.weights", "models/yolov3-tiny.cfg")

# Load COCO names 
classes1 = []
with open("models/coco.names", "r") as f:
    classes1 = [line.strip() for line in f]

# Set the target classes
target_classes = ['bottle', 'apple', 'cup', 'orange', 'banana']

# Establish connection with arm
arm = XArm()

# Connect to camera
cap = cv2.VideoCapture(0)
cap.set(3, 320)
cap.set(4, 240)
cap.set(cv2.CAP_PROP_FPS, 1) # 1 frame per second
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 1 frame buffer

# Measure the frames and buffer flag
frameCount = 0
get_rid_of_buffer = False

while True:
    
    # Get the frame
    _, frame = cap.read()

    if (get_rid_of_buffer):
        print("got rid of buffer")
        get_rid_of_buffer = False
        continue

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
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.1 and classes1[class_id] in target_classes:
                
                # Object detected
                print(f"{classes1[class_id]} detected with confidence {confidence}")

                # Draw bounding box
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Activate the arm
                activateArm(classes1[class_id])
                found_detection = True
                print("breaking out of inner")
                break  # Exit the inner loop
        else:
            continue
        get_rid_of_buffer = True
        break

    # Save the frame to the "pictures" folder
    #image_filename = f"pictures/frame{frameCount}.png"
    #cv2.imwrite(image_filename, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

