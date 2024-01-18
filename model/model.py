from ultralytics import YOLO
import torch

class ModelYOLO:
    def __init__(self, model_path, device='cuda'):
        self.model = YOLO(model_path)
        self.start(device)
        
    def start(self, device):   
        if device == 'cuda':
            torch.cuda.set_device(0)
            self.model.to(device)
        else:
            print("Not using CUDA")
            self.model.to(torch.device('cpu'))
        self.model.fuse()
        self.dict_classes = self.model.model.names
        self.class_ids = [2, 3, 5, 7, 67] 

    def predict(self, image, conf = 0.1, classes = None):
        classes = self.class_ids if classes is None else classes
        return self.model.predict(image, conf = conf, classes = classes, verbose=False, device=0)

def predict_handler(predict):
    df = pd.DataFrame(predict[0].cpu().numpy().boxes.data, columns = ['xmin', 'ymin', 'xmax', 'ymax', 'conf', 'class']).astype('float')
    df['center_x'] = df['xmin'] + (df['xmax'] - df['xmin'])*float(os.getenv('CENTER_PERCENTAGE_X'))
    df['center_y'] = df['ymin'] + (df['ymax'] - df['ymin'])*float(os.getenv('CENTER_PERCENTAGE_Y'))
    return df