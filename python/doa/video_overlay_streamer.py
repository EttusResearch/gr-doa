import cv2

# make sure you have permission to access the camera
# chmod 666 /dev/video0

def find_available_camera():
    """Find the first available camera index"""
    for i in range(5):  # Check camera indices 0-4
        print(f"Trying camera index {i}...")
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            cap.release()
            if ret:
                print(f"Found working camera at index {i}")
                return i
        cap.release()
    return None

cv2.namedWindow("preview")

# Find available camera
camera_index = find_available_camera()


if camera_index is None:
    print("Error: No working cameras found!")
    print("Please check:")
    print("1. Is a camera connected?")
    print("2. Is the camera being used by another application?")
    print("3. Do you have permission to access the camera?")
    cv2.destroyWindow("preview")
    exit(1)

vc = cv2.VideoCapture(camera_index)

width = 1920
height = 1080

# Set video capture properties
vc.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# height and width of overlay
w = width//3 
h = height//2

# distance to top left corner
x = width//2 - w//2
y = height//2 - h//2


if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
    if not rval:
        print("Error: Camera opened but couldn't read frame")
        vc.release()
        cv2.destroyWindow("preview")
        exit(1)
else:
    print("Error: Could not open camera after detection")
    vc.release()
    cv2.destroyWindow("preview")
    exit(1)

while rval:
    # Draw a rectangle for overlay
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)  
    cv2.imshow("preview", frame)
    rval, frame = vc.read()

    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break

vc.release()
cv2.destroyWindow("preview")