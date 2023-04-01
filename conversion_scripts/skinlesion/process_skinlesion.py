import shutil
import os
import random
import numpy as np
import pandas as pd

def process_skinlesion(dst_path):
    # Remove the previous skinlesion folder
    if os.path.exists(dst_path):
        remove = input(f"Removing '{os.path.abspath(dst_path)}', because it already exists. Are you sure of it? (Y or N) ")
        if remove.upper() == "Y" :
            shutil.rmtree(dst_path)
        elif remove.upper() == "N":
            exit()
        else:
            raise Exception("Invalid Answer")
    
    # Tupple with the name of the splits that we will create
    splits = ("train", "val", "test", "full")

    # Read the csv files that contain the ground truth classes of each image
    train_gt_path = "ISIC2018_Task3_Training_GroundTruth" 
    train_images_path = "ISIC2018_Task3_Training_Input" 

    val_gt_path = "ISIC2018_Task3_Validation_GroundTruth" 
    val_images_path = "ISIC2018_Task3_Validation_Input"

    train_gt = pd.read_csv(f"{train_gt_path}/ISIC2018_Task3_Training_GroundTruth.csv")
    val_gt = pd.read_csv(f"{val_gt_path}/ISIC2018_Task3_Validation_GroundTruth.csv")
    classes = list(train_gt.columns[1:]) 

    # Create skinlesion folder (Folder of the processed dataset)
    os.mkdir(dst_path)

    # Create data folder
    data_path = os.path.join(dst_path, "data")
    os.mkdir(data_path)

    # Create all the split folders in the skinlesion dataset folder
    # Inside that folders, create a folder for each class
    # split_cls_paths dictionary save the paths of each class folder created 
    split_cls_paths = {}
    for split in splits:
        split_path = os.path.join(data_path, split)
        os.mkdir(split_path)
        split_cls_paths[split] = {}
        for cls in classes:
            cls_path = os.path.join(split_path, cls)
            os.mkdir(cls_path)
            split_cls_paths[split][cls] = cls_path
    
    for cls in classes:
        # Get the row of the csv files that correspond to cls class
        train_cls_rows = train_gt.loc[train_gt[cls]==1.0].reset_index(drop=True)
        val_cls_rows = val_gt.loc[val_gt[cls]==1.0].reset_index(drop=True)

        # Get the names of the images 
        train_cls_image_names = train_cls_rows['image']
        val_cls_image_names = val_cls_rows['image']

        # Create the image paths
        train_cls_image_paths = [f"{train_images_path}/{image_name}.jpg" for image_name in train_cls_image_names]
        val_cls_image_paths = [f"{val_images_path}/{image_name}.jpg" for image_name in val_cls_image_names]

        # Join the train and validation original partitions
        cls_image_paths = train_cls_image_paths + val_cls_image_paths

        # Shuffle the images
        random.shuffle(cls_image_paths)

        # Split the images paths in train, val and test partitions, according to a rule of 60% / 20% / 20%
        train, val, test = np.split(cls_image_paths, [int(len(cls_image_paths)*0.6), int(len(cls_image_paths)*0.8)])

        # Copy the images to the new corresponding folder
        for path in train:
            shutil.copy(path, split_cls_paths["train"][cls] )
            shutil.copy(path, split_cls_paths["full"][cls] )
        
        for path in val:
            shutil.copy(path, split_cls_paths["val"][cls])
            shutil.copy(path, split_cls_paths["full"][cls] )

        for path in test:
            shutil.copy(path, split_cls_paths["test"][cls])
            shutil.copy(path, split_cls_paths["full"][cls] )
            
    print()
    print("'skinlesion' dataset - Ready to be used in this Benchmark.")
    print()

if __name__ == "__main__":
    process_skinlesion("./skinlesion")
