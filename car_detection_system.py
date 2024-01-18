from model.model import ModelYOLO, predict_handler
from utils.cv_utils import resize_frame, process_file, display_image
from utils.mask import get_all_masks, mask_colorize, join_masks
from park_manager import ParkingManager
import numpy as np
import cv2
import time
import os


class CarDetectionSystem:
    def __init__(self, model_path, device='cuda'):
        self.model = ModelYOLO(model_path, device=device)
        self.park = ParkingManager()
        self.start()

    def start(self):
        masks = get_all_masks(os.getenv('MASKS_PATH', "./data/masks/"))
        for k, mask in masks.items():
            self.park.set_parking_space(k, mask)

    def predict(self, image):
        results = self.model.predict(image, conf = float(os.getenv('CONF', '0.4')))
        df = predict_handler(results)
        return df
    
    def update_parking_spaces(self, image):
        self.reset()
        df = self.predict(image)
        self.df_state = df
        for i in range(len(df)):
            center_x, center_y = df[['center_x', 'center_y']].iloc[i].astype('int')
            self.park.point_in_parking_space((center_x, center_y))

    def display(self, image):
        image = image.copy()
        if self.df_state is None: return
        occupied_masks = self.park.get_masks(occupied=True)
        free_masks = self.park.get_masks(occupied=False)
        occupied_color = (0,0,255)
        free_color = (0,255,0)

        occupied_mask = join_masks(occupied_masks)
        free_mask = join_masks(free_masks)
        
        if occupied_mask is not None:
            image = cv2.addWeighted(image, 0.7, mask_colorize(image, occupied_mask, color=occupied_color), 0.3, 0)
        if free_mask is not None:
            image = cv2.addWeighted(image, 0.7, mask_colorize(image, free_mask, color=free_color), 0.3, 0)


        for i in range(len(self.df_state)):
            xmin, ymin, xmax, ymax, _, class_id, center_x, center_y = self.df_state.iloc[i].astype('int')
            confidence = self.df_state['conf'].iloc[i]
            label = self.model.dict_classes[class_id]
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (255,0,0), 1) 
            cv2.circle(image, (center_x,center_y), 1,(0,0,255),-1) 
            cv2.putText(img=image, text=label +' - '+str(np.round(confidence,2)),
                            org= (xmin,ymin-10), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.5, color=(255, 0, 0),thickness=1)
        # cv2.imshow("Image", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return image


    def reset(self):
        self.df_state = None
        self.park.set_all_parking_spaces_empty()

    