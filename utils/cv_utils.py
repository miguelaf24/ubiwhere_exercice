import cv2

def resize_frame(frame, scale_percent):
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    return resized

def process_video(video_name):
    cap = cv2.VideoCapture(video_name)

    if not cap.isOpened():
        raise("Error opening the video.")

    ret, frame = cap.read()
    if not ret:
        raise Exception("Error reading the video.")

    return frame

def process_image(image_name):
    image = cv2.imread(image_name)

    if image is None:
        raise Exception("Error opening the image.")

    return image

def process_file(file_path):
    if file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
        return process_video(file_path)
    elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        return process_image(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a video (.mp4, .avi, .mkv, .mov) or an image (.jpg, .jpeg, .png, .bmp).")
    
def display_image(image, window_name='Image'):
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

