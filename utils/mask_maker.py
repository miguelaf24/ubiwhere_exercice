import argparse
from mask import mask_maker
from cv_utils import process_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a video or image and create mask files.")
    parser.add_argument("file_path", type=str, help="Path to the video file or image")
    parser.add_argument("masks_dir", type=str, nargs='?', default="./data/masks", help="Directory to save masks (optional)")

    args = parser.parse_args()
    
    # print(args.file_path)
    image = process_file(args.file_path)
    
    mask_maker(image, args.masks_dir)