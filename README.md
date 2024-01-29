# Exercise Ubiwhere - Parking Detection Project

This project was developed as part of a computer vision exercise for Ubiwhere, focusing on the detection of occupied parking spaces.

## Getting Started
To use this program, follow the steps below:

## Step 1: Create Parking Space Masks
Before running the main program, it is necessary to create masks for the parking spaces. To facilitate this process, a script `./utils/mask_maker.py` has been developed. This script allows you to mark the parking spaces on the images, creating the necessary masks.

Run the script: `python ./utils/mask_maker.py path_image`

![example_mask_maker](https://raw.githubusercontent.com/miguelaf24/ubiwhere_exercice/main/docs/mask_maker.png)
To create the masks for the designated areas, one must utilize mouse clicks. 

Save each parking space individually. 

- "space" - to save the park space
- "c" - to delete the current drawing
- "esc" - to exit

rename the files with the desired parking space ID.

## Step 2: Build and Run Docker
~~Run the following command to build the Docker images:~~

~~`docker-compose build`~~

~~Once the images are built, run the Docker containers with the following command:~~

~~`docker-compose up`~~

Note: I couldn't get the Docker service to work correctly because i had TensorFlow CUDA issues. The model responded with: `{
	"detail": "Invalid CUDA 'device=0' requested. Use 'device=cpu' or pass valid CUDA device(s) if available, i.e. 'device=0' or 'device=0,1,2,3' for Multi-GPU.\n\ntorch.cuda.is_available(): False\ntorch.cuda.device_count(): 0\nos.environ['CUDA_VISIBLE_DEVICES']: None\nSee https://pytorch.org/get-started/locally/ for up-to-date torch install instructions if no CUDA devices are seen by torch.\n"
}`

So you will need to run locally.

To install Python dependencies:
`pip install --no-cache-dir -r requirements.txt`

To run service `python app.py`




## Step 3: Send Images to Service
Open the `Insomnia` or `Postman` to interact with the API and prepare the request:
- Method: POST
~~ - URL: http://localhost:8080/api/parking_spaces ~~
- URL: http://localhost:5000/api/parking_spaces 
- Body: Select "form-data" and add a key-value pair with key=image and value=your_image_file.

### Endpoints
- /api/test_image
    -> send the image and recive the same image, just for check if service works
- /api/parking_spaces
    -> send image of park, it must be of the same resolution and related to the same parking lot. It will response with a dictionary

- /api/parking_spaces_image



# Development and Algorithmics

The `./utils/mask_maker.py` was developed to draw polygons for defining parking spaces. This script allows the user to draw polygons on the image using mouse clicks. The drawn polygons are saved as masks in the specified directory.

The primary application is `app.py`, serving as a restAPI that receives an image, as described in the previous "Endpoints". This API interacts with a `CarDetectionSystem` object, responsible for determining car positions using the `ModelYOLO`. Subsequently, it assesses parking space occupancy through the `ParkingManager` object.

The `ModelYOLO` class utilizes the [Ultralytics YOLO framework](https://docs.ultralytics.com/) to perform car detection. It initializes with a specified YOLO model and device. The `predict` method predicts car positions in an image with adjustable confidence and class filtering. The `predict_handler` function post-processes prediction results, converting them into a DataFrame with additional columns for object centers based on environmental settings.

The `ParkingManager` class manages parking spaces, allowing setting, retrieval, and analysis of occupancy status. It provides methods to obtain total, occupied, and free parking spaces, along with occupancy percentages. The class can reset all parking spaces to unoccupied. Additionally, it includes functionality to identify a parking space based on a given point. The `ParkingSpace` class represents an individual parking space, holding attributes for its ID, occupancy status, and mask. The `is_point_in_mask` method changes the occupancy status of the parking space.

# Future Work
- Docker Service with CUDA:
Future work includes containerizing the application as a Docker service with CUDA support, optimizing performance for GPU-accelerated tasks.

- Enhanced Point-in-Image Algorithm:
Further development aims to refine the algorithm determining whether a point is within an image. This improvement will enhance accuracy and efficiency in identifying parking space occupancy.

- 3D Bounding Box Detection:
An upcoming feature involves implementing a 3D bounding box detection system. This will assess the car's position on the ground, ensuring proper parking space occupation assessment by considering spatial dimensions.
