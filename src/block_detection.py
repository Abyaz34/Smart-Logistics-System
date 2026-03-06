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

cap = cv2.VideoCapture(0)

last_center = None
stable_start_time = None
STABLE_THRESHOLD = 3  # seconds
current_color = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

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
                roi = frame[y:y+h, x:x+w]
                result = reader.readtext(roi)

                print(f"\nDetected Color: {current_color}")
                print(f"Color Confidence: {color_confidence:.3f}")

                if len(result) == 0:
                    print("Detected Text: NONE")
                    ocr_conf = 0
                else:
                    ocr_conf = np.mean([r[2] for r in result])
                    print("Detected Text:")
                    for r in result:
                        print(r[1])

                # Compute reliability score
                stability_score = min(elapsed / STABLE_THRESHOLD, 1)
                reliability = (0.4 * color_confidence) + (0.3 * ocr_conf) + (0.3 * stability_score)

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