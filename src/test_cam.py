# src/test_cam.py
import cv2

# Try to open the default webcam (index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    exit()

print("Webcam test started ✅")
print("Press 'q' to quit.")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Flip horizontally for mirror view
    frame = cv2.flip(frame, 1)

    # Display the frame
    cv2.imshow("Webcam Test", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release and close
cap.release()
cv2.destroyAllWindows()
