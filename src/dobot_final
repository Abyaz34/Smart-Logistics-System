from pydobot import Dobot
from serial.tools import list_ports
import time
import cv2
import numpy as np

# --- 1. Define Your Coordinates (X, Y, Z, R) ---

HOME = (213.15, 90.37, 166.78, 0)

# Pick up location
PICK_UP_TOP = (211.34, 152.35, 132.28, 0)
PICK_UP     = (146.16, 127.07, 26.43, 0)

# Camera inspection location
CAMERA_TOP  = (58.76, 269.31, 141.20, 0)
CAMERA      = (68.57, 295.85, 51.71, 0)

# Conveyor belt drop-off location
CONVEYOR_TOP  = (159.21, -240.67, 128.31, 0)
CONVEYOR_DROP = (178.11, -235.86, 31.60, 0)

# NEW : RED block drop location
RED_TOP  = (184.5, -201.45, 100, 0)
RED_DROP = (184.5, -201.45, 20, 0)

# --- 2. Connect to the Dobot ---

available_ports = list_ports.comports()

if not available_ports:
    print("No Dobot detected. Check your USB connection or close DobotStudio.")
    exit()

port = available_ports[0].device
print(f"Connecting to Dobot on port {port}...")

device = Dobot(port=port, verbose=False)

# --- 3. Camera Setup ---

cap = cv2.VideoCapture(0)

def detect_red():

    ret, frame = cap.read()

    if not ret:
        return False

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # red ranges
    lower_red1 = np.array([0,120,70])
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([170,120,70])
    upper_red2 = np.array([180,255,255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    red_pixels = cv2.countNonZero(mask)

    if red_pixels > 3000:
        return True

    return False


# --- 4. Execute the Sequence ---

try:

    print("Starting sequence...")

    # 1. Move to home
    device.move_to(*HOME, wait=True)

    # 2. Pick up (suction ON)
    device.move_to(*PICK_UP, wait=True)
    device.suck(True)
    time.sleep(0.5)

    # 3. Pick up top
    device.move_to(*PICK_UP_TOP, wait=True)

    # 4. Camera top
    device.move_to(*CAMERA_TOP, wait=True)

    # 5. Camera inspection
    device.move_to(*CAMERA, wait=True)
    time.sleep(1)

    print("Checking block color...")

    is_red = detect_red()

    # 6. Camera top
    device.move_to(*CAMERA_TOP, wait=True)

    # --- IF RED BLOCK ---
    if is_red:

        print("RED block detected!")

        device.move_to(*RED_TOP, wait=True)
        device.move_to(*RED_DROP, wait=True)

        device.suck(False)
        time.sleep(0.5)

        device.move_to(*RED_TOP, wait=True)

    # --- OTHERWISE DROP ON CONVEYOR ---
    else:

        print("Not red → sending to conveyor")

        device.move_to(*HOME, wait=True)

        device.move_to(*CONVEYOR_TOP, wait=True)
        device.move_to(*CONVEYOR_DROP, wait=True)

        device.suck(False)
        time.sleep(0.5)

        device.move_to(*CONVEYOR_TOP, wait=True)

    # 11. Home
    device.move_to(*HOME, wait=True)

    print("Sequence complete!")

except Exception as e:

    print(f"An error occurred: {e}")

finally:

    # --- 5. Safely Disconnect ---
    device.suck(False)

    device.close()

    cap.release()

    print("Disconnected safely.")