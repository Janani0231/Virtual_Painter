# src/main.py
import cv2
import numpy as np

# --- Adjustable HSV color range (example: green marker) ---
# You will likely need to tune these values using mask_tuner.py
lower_hsv = np.array([40, 70, 70])
upper_hsv = np.array([80, 255, 255])

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Create a blank white canvas (same size as video feed)
ret, frame = cap.read()
if not ret:
    print("Error: Cannot access webcam")
    cap.release()
    exit()

canvas = np.ones_like(frame) * 255   # White canvas
points = []  # Store marker positions

print("Virtual Painter started 🎨")
print("Press 'c' to clear the canvas, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally (mirror view)
    frame = cv2.flip(frame, 1)

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask for marker color
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours and len(contours) > 0:
        # Largest contour
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > 500:  # filter small noise
            (x, y, w, h) = cv2.boundingRect(c)
            cx = x + w // 2
            cy = y + h // 2
            points.append((cx, cy))

    # Draw on the canvas
    for i in range(1, len(points)):
        if points[i - 1] is None or points[i] is None:
            continue
        cv2.line(canvas, points[i - 1], points[i], (0, 0, 255), 5)

    # Overlay canvas on the live video feed
    combined = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Show windows
    cv2.imshow("Virtual Painter - Live Feed", combined)
    cv2.imshow("Mask", mask)

    # Key controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.ones_like(frame) * 255
        points = []

cap.release()
cv2.destroyAllWindows()
