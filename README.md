# Exercice Ubiwhere - Parking Detection Project

This project was developed as part of a computer vision exercise for Ubiwhere, focusing on the detection of occupied parking spaces.

## Getting Started
To use this program, follow the steps below:

## Step 1: Create Parking Space Masks
Before running the main program, it is necessary to create masks for the parking spaces. To facilitate this process, a script named `mask_maker.py` has been developed. This script allows you to mark the parking spaces on the images, creating the necessary masks.

Run the script: `python ./utils/mask_maker.py path_image`

![example_mask_maker](https://raw.githubusercontent.com/miguelaf24/ubiwhere_exercice/main/docs/mask_maker.png)
To create the masks for the designated areas, one must utilize mouse clicks. 

Save each parking space individually. 

To save, press the "space" key, and to delete the current drawing, press "c". 

Upon completion press "Esc", rename the files with the desired parking space ID.

## Step 2: Build and Run Docker


`docker-compose build`

`docker-compose up`

## Step 3: Send Images to Service
`Insomnia` to interact with the API and 


[Ultralytics](https://docs.ultralytics.com/)