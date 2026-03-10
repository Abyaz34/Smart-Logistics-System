import cv2
import numpy as np
import easyocr
import time
import csv
import os

from datetime import datetime

# Initialize CSV
CSV_FILE = 'log.csv'

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Color", "Text", "Category", "Reliability"]) 

# Initialize OCR
reader = easyocr.Reader(['en'])

# Color ranges in HSV
color_ranges = {
    "RED": [(0, 120, 70), (10, 255, 255)],
    "RED2": [(170, 120, 70), (180, 255, 255)],
    "GREEN": [(36, 50, 70), (89, 255, 255)],
    "YELLOW": [(15, 100, 100), (35, 255, 255)]
}

# Function for logging to CSV
def log_to_csv(color, text, reliability):
    timestamp = datetime.now().strftime("%H:%M:%S")
    category = f"{color}-{text}" if text else color
    
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, color, text, category, f"{reliability:.2f}"])
    print(f"--> LOGGED: {category}")


cap = cv2.VideoCapture(0)

last_center = None
stable_start_time = None
STABLE_THRESHOLD = 1
current_color = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Clean copy for OCR
    frame_for_ocr = frame.copy()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detected_box = None
    current_color = None
    color_confidence = 0

    # Detect each color
    for color_name, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 2000:
                x, y, w, h = cv2.boundingRect(cnt)
                detected_box = (x, y, w, h)
                current_color = color_name.replace("2", "")

                # Compute color confidence
                roi_mask = mask[y:y+h, x:x+w]
                non_zero = cv2.countNonZero(roi_mask)
                total_pixels = w * h
                color_confidence = non_zero / total_pixels

                # Draw bounding box
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 255), 2)
                cv2.putText(frame, f"{current_color} ({color_confidence*100:.1f}%)",
                            (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                            (255, 255, 255), 2)

    # Stability check
    if detected_box:
        x, y, w, h = detected_box
        center = (x + w//2, y + h//2)

        if last_center is None:
            last_center = center
            stable_start_time = time.time()

        if abs(center[0] - last_center[0]) < 5 and abs(center[1] - last_center[1]) < 5:
            elapsed = time.time() - stable_start_time

            cv2.putText(frame, f"Stable: {elapsed:.1f}s",
                        (20, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

            if elapsed >= STABLE_THRESHOLD:
                roi = frame_for_ocr[y:y+h, x:x+w]
                result = reader.readtext(roi)

                print(f"\nDetected Color: {current_color}")
                print(f"Color Confidence: {color_confidence:.3f}")

                detected_text = ""

                if len(result) == 0:
                    print("Detected Text: NONE")
                    detected_text = "NONE"
                    ocr_conf = 0
                else:
                    ocr_conf = np.mean([r[2] for r in result])
                    print("Detected Text:")
                    
                    text_parts = []
                    for r in result:
                        print(r[1]) 
                        text_parts.append(r[1])

                    detected_text = " ".join(text_parts)

                # Compute reliability score
                stability_score = min(elapsed / STABLE_THRESHOLD, 1)
                reliability = (0.4 * color_confidence) + (0.3 * ocr_conf) + (0.3 * stability_score)

                # Log to CSV
                log_to_csv(current_color, detected_text, reliability)

                print(f"OCR Confidence: {ocr_conf:.3f}")
                print(f"Reliability Score: {reliability:.3f}")

                stable_start_time = time.time() + 999

        else:
            stable_start_time = time.time()

        last_center = center

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()