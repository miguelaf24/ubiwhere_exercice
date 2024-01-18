import cv2
import numpy as np
import os

def create_mask(image, polygon, mask_id, save_path='./data/masks'):
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.fillPoly(mask, [np.array(polygon)], 255)

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    mask_filename = os.path.join(save_path, f'mask_{mask_id}.png')
    cv2.imwrite(mask_filename, mask)
    return mask

def load_masks(mask_directory):
    masks = []
    for filename in os.listdir(mask_directory):
        if filename.endswith(".png"):
            mask_id = filename.split(".")[0]
            mask_path = os.path.join(mask_directory, filename)
            mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)
            masks.append({'id': mask_id, 'mask': mask, 'mask_path': mask_path})
    return masks, len(masks)

def mask_maker(image, mask_directory = './data/masks'):
    if image is None:
        raise("Error loading the image.")

    image_with_rois = image.copy()
    masks, last_mask_id = load_masks(mask_directory)

    polygon = []

    def draw_polygon(event, x, y, flags, param):
        nonlocal polygon, image_with_rois

        if event == cv2.EVENT_LBUTTONDOWN:
            polygon.append((x, y))
            if len(polygon) > 1:
                cv2.line(image_with_rois, polygon[-2], polygon[-1], (0, 255, 0), 2)
            if len(polygon) > 2:
                cv2.polylines(image_with_rois, [np.array(polygon, dtype=np.int32)], isClosed=False, color=(0, 255, 0), thickness=2)
            cv2.imshow("Image with ROIs", image_with_rois)
            

    cv2.namedWindow("Image with ROIs")
    cv2.setMouseCallback("Image with ROIs", draw_polygon)
    cv2.imshow("Image with ROIs", image_with_rois)
    backup_image = image_with_rois.copy()
    while True:
        key = cv2.waitKey(0) & 0xFF

        if key == 27:
            break

        if key == 32:  # 'space' for save
            if len(polygon) > 2:
                last_mask_id += 1
                mask = create_mask(image, np.array([polygon], dtype=np.int32), last_mask_id, save_path=mask_directory)
                masks.append({'id': last_mask_id, 'mask': mask})
                polygon = []  
                cv2.imshow("Image with ROIs", image_with_rois)
                backup_image = image_with_rois.copy()
        elif key == ord('c'):  # 'c' for clear
            image_with_rois = backup_image.copy()
            polygon = []
            cv2.imshow("Image with ROIs", image_with_rois)

        if cv2.getWindowProperty("Image with ROIs", cv2.WND_PROP_VISIBLE) < 1:
            break

    for mask_data in masks:
        print(f"Mask ID: {mask_data['id']}")

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_all_masks(masks_folder):
    masks = {}
    mask_files = [file for file in os.listdir(masks_folder) if file.endswith(('.png', '.jpg', '.jpeg'))]
    for mask_file in mask_files:
        mask_id = mask_file.split('.')[0]
        mask_path = os.path.join(masks_folder, mask_file)
        masks[mask_id] = cv2.imread(mask_path)
    return masks

def mask_colorize(image, mask, color=(0, 255, 0)):
    _, mask = cv2.threshold(mask, thresh=180, maxval=255, type=cv2.THRESH_BINARY)
    colorized_mask = np.copy(image)
    colorized_mask[(mask==255).all(-1)] = [color]
    return colorized_mask

def join_masks(masks):
    if not masks:
        return None
    mask = masks[0]
    for i in range(1, len(masks)):
        mask = cv2.bitwise_or(mask, masks[i])
    return mask
