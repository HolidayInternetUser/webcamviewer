import os
import cv2
import keyboard

home_dir = os.path.expanduser("~")
footage_dir = os.path.join(home_dir, "Webcam_Footage")
os.makedirs(footage_dir, exist_ok=True)

base_filename = "webcam_footage.avi"
file_index = 1
file_path = os.path.join(footage_dir, base_filename)
while os.path.exists(file_path):
    file_path = os.path.join(footage_dir, f"webcam_footage_{file_index}.avi")
    file_index += 1

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not capture.isOpened():
    print("Error: Could not open webcam.")
    exit()

frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(file_path, fourcc, 20.0, (frame_width, frame_height))

window_visible = True

while True:
    ret, frame = capture.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    out.write(frame)
    
    if window_visible:
        cv2.imshow("Webcam (Alt+H: Hide, Alt+S: Show, ESC: Exit)", frame)
    
    if keyboard.is_pressed("alt+h"):
        window_visible = False
        cv2.destroyAllWindows()
    elif keyboard.is_pressed("alt+s") and not window_visible:
        window_visible = True
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()
out.release()
cv2.destroyAllWindows()

print(f"Footage saved to: {file_path}")