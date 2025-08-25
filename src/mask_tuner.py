# src/mask_tuner.py
import cv2
import numpy as np

def nothing(x):
    pass

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Cannot access webcam")
    exit()

# Create a window
cv2.namedWindow("Trackbars")

# Create trackbars for HSV values
cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)   # Lower Hue
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)   # Lower Saturation
cv2.createTrackbar("LV", "Trackbars", 0, 255, nothing)   # Lower Value
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing) # Upper Hue
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing) # Upper Saturation
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing) # Upper Value

print("HSV Mask Tuner started 🎛️")
print("Adjust sliders to detect your marker color.")
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get current positions of trackbars
    lh = cv2.getTrackbarPos("LH", "Trackbars")
    ls = cv2.getTrackbarPos("LS", "Trackbars")
    lv = cv2.getTrackbarPos("LV", "Trackbars")
    uh = cv2.getTrackbarPos("UH", "Trackbars")
    us = cv2.getTrackbarPos("US", "Trackbars")
    uv = cv2.getTrackbarPos("UV", "Trackbars")

    lower_hsv = np.array([lh, ls, lv])
    upper_hsv = np.array([uh, us, uv])

    # Mask and result
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show results
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered", result)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
