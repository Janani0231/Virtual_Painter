# src/utils.py
import cv2
import numpy as np

def find_marker_center(mask, min_area=500):
    """
    Find the largest contour in the mask and return its center coordinates.
    :param mask: Binary mask from HSV thresholding
    :param min_area: Minimum contour area to filter noise
    :return: (x, y) center of the marker or None if not found
    """
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    # Find the largest contour
    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < min_area:
        return None

    # Bounding box and centroid
    (x, y, w, h) = cv2.boundingRect(c)
    cx = x + w // 2
    cy = y + h // 2
    return (cx, cy)


def draw_strokes(canvas, points, color=(0, 0, 255), thickness=5):
    """
    Draw continuous strokes on the canvas from a list of points.
    :param canvas: The image (canvas) to draw on
    :param points: List of (x, y) tuples
    :param color: Stroke color in BGR
    :param thickness: Stroke thickness
    :return: Updated canvas
    """
    for i in range(1, len(points)):
        if points[i - 1] is None or points[i] is None:
            continue
        cv2.line(canvas, points[i - 1], points[i], color, thickness)
    return canvas


def overlay_canvas(frame, canvas, alpha=0.5):
    """
    Blend the live video frame with the canvas.
    :param frame: Original webcam frame
    :param canvas: Drawing canvas
    :param alpha: Transparency factor (0.0–1.0)
    :return: Combined image
    """
    return cv2.addWeighted(frame, alpha, canvas, 1 - alpha, 0)
