import cv2
import numpy as np
import easyocr
import time

# Initialize OCR
reader = easyocr.Reader(['en'])

# Color ranges in HSV
color_ranges = {
    "RED": [(0, 120, 70), (10, 255, 255)],
    "RED2": [(170, 120, 70), (180, 255, 255)],
    "GREEN": [(36, 50, 70), (89, 255, 255)],
    "YELLOW": [(15, 100, 100), (35, 255, 255)]
}

cap = cv2.VideoCapture(0) # change to 1 when using external webcame

last_center = None
stable_start_time = None
STABLE_THRESHOLD = 3  # seconds
current_color = None  # store detected color

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detected_box = None
    current_color = None

    # Detect each color
    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:  # filter noise
                x, y, w, h = cv2.boundingRect(cnt)
                detected_box = (x, y, w, h)
                current_color = color_name.replace("2", "")  # RED2 → RED

                # Draw bounding box + color label
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(frame, current_color, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Stability check
    if detected_box:
        x, y, w, h = detected_box
        center = (x + w//2, y + h//2)

        if last_center is None:
            last_center = center
            stable_start_time = time.time()

        # Check if center moved
        if abs(center[0] - last_center[0]) < 5 and abs(center[1] - last_center[1]) < 5:
            elapsed = time.time() - stable_start_time

            # Show timer on screen
            cv2.putText(frame, f"Stable: {elapsed:.1f}s",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

            if elapsed >= STABLE_THRESHOLD:
                roi = frame[y:y+h, x:x+w]
                result = reader.readtext(roi)

                print(f"Detected Color: {current_color}")
                print("Detected Text:")
                if len(result) == 0:
                    print("NONE")
                else:
                    for r in result:
                        print(r[1])

                stable_start_time = time.time() + 999  # prevent repeated reading

        else:
            stable_start_time = time.time()

        last_center = center

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): # to exit press q
        break

cap.release()
cv2.destroyAllWindows()