import cv2
import numpy as np

class ParkingManager():
    def __init__(self):
        self.parking_spaces = {}

    def set_parking_space(self, id, mask, occupied=False):
        self.parking_spaces[id] = ParkingSpace(id, mask, occupied)
    
    def get_parking_spaces(self, occupied=False):
        return [space.id for space in self.parking_spaces.values() if space.occupied == occupied]
    
    def get_masks(self, occupied=False):
        return [space.mask for space in self.parking_spaces.values() if space.occupied == occupied]

    def get_total_parking_spaces(self):
        return len(self.parking_spaces)
    
    def __repr__(self):
        return str(self.__dict__())
        
        
    def __dict__(self):
        total_spaces = self.get_total_parking_spaces()
        occupied_spaces = self.get_parking_spaces(occupied=True)
        free_spaces = self.get_parking_spaces(occupied=False)
        free_count = len(free_spaces)
        occupied_count = len(occupied_spaces)
        lotation_percent = occupied_count/total_spaces
        lotation_str = f"{occupied_count}/{total_spaces}"        
        dict = {
            "total_spaces":total_spaces,
            "occupied_spaces":occupied_spaces,
            "free_spaces":free_spaces,
            "free_count":free_count,
            "occupied_count":occupied_count,
            "lotation_percent":lotation_percent,
            "lotation_str":lotation_str
        }
        return dict

    def set_all_parking_spaces_empty(self):
        for space in self.parking_spaces.values():
            space.occupied = False

    def point_in_parking_space(self, point):
        for space in self.get_parking_spaces(occupied=False):
            if self.parking_spaces[space].is_point_in_mask(point):
                return space

class ParkingSpace:
    def __init__(self, id, mask=None, occupied=False):
        self.id = id
        self.occupied = occupied
        self.mask = mask

    def is_point_in_mask(self, point):
        if self.occupied:
            print("The parking space is already occupied.")
            return None
        point_x, point_y = point
        self.occupied = sum(self.mask[point_y, point_x]) > 0
        return self.occupied
        



    
