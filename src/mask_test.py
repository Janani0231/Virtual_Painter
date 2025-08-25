# src/mask_test.py
import cv2
import numpy as np

# --- Example HSV color range (green marker) ---
# You should adjust these values for your marker
lower_hsv = np.array([40, 70, 70])
upper_hsv = np.array([80, 255, 255])

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam")
    exit()

print("Mask Test started ✅")
print("Press 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror view
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask for the chosen color
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Apply mask to the original frame
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Show original, mask, and result
    cv2.imshow("Original", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Filtered", result)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
