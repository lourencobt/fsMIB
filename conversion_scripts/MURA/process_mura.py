import math
import shutil
import os
import random
import numpy as np
import pandas as pd

r_state = np.random.RandomState()

# Function that given a dataframe of images paths, copies them to dst_path with a new name according to counter
def copy_full(dataframe, dst_path, counter):
    first_column = dataframe.columns[0]
    # copy train to train folder and val to Validation folder
    
    for idx in dataframe.index:
        path = dataframe[first_column][idx]
        counter += 1
        dst_normal_test_path = os.path.join(dst_path, f"{counter}"+".png")
        shutil.copy(path, dst_normal_test_path )
    
    return counter


# Function that given a dataframe of images paths, copies them to dst_path with a new name
def copy(dataframe, dst_path):
    first_column = dataframe.columns[0]
    # copy train to train folder and val to Validation folder
    
    counter = 0
    for idx in dataframe.index:
        path = dataframe[first_column][idx]
        counter += 1
        dst_normal_test_path = os.path.join(dst_path, f"{counter}"+".png")
        shutil.copy(path, dst_normal_test_path )

# Function to randomize dataframe rows
def randomize(dataframe):
    dataframe=dataframe.sample(frac=1, random_state=r_state).reset_index(drop=True)
    
    return dataframe

def process_mura(src_path, dst_path):
    counter_full = 0
    types = ('elbow', 'finger', 'forearm', 'hand', 'humerus', 'shoulder', 'wrist')
    splits = ("train", "val", "test", "full")

    if os.path.exists(dst_path):
        remove = input(f"Removing '{os.path.abspath(dst_path)}', because it already exists. Are you sure of it? (Y or N) ")
        if remove.upper() == "Y" :
            shutil.rmtree(dst_path)
        elif remove.upper() == "N":
            exit()
        else:
            raise Exception("Invalid Answer")
    
    # Create mura folder (Folder of the processed dataset)
    os.mkdir(dst_path)

    # Create Necessary folders per type 
    # The necessary folders are the data folder that inside have the splits folders that inside have the classes per splits folders
    data_folders_paths = {}
    for t in types:
        type_folder_path = os.path.join(dst_path, t)
        os.mkdir(type_folder_path)
       
        data_folder_path = os.path.join(type_folder_path,'data')
        os.mkdir(data_folder_path)
        data_folders_paths[t] = data_folder_path

        splits_paths = []
        for split in splits:
            path = os.path.join(data_folder_path, split)
            os.mkdir(path)
            splits_paths.append(path)

        # Create folders for classes
        for split_path in splits_paths:
            normal_path = os.path.join(split_path, "normal")
            os.mkdir(normal_path)

            abnormal_path = os.path.join(split_path, "abnormal")
            os.mkdir(abnormal_path)

    # Read the paths of the testing images
    test_image_paths = pd.read_csv('MURA-v1.1/valid_image_paths.csv')
    first_column = test_image_paths.columns[0]
    test_image_paths.rename(columns={first_column:"test_image_paths"}, inplace=True)

    # Read the paths of the training images
    trainval_image_paths = pd.read_csv('MURA-v1.1/train_image_paths.csv')
    first_column = trainval_image_paths.columns[0]
    trainval_image_paths.rename(columns={first_column:"train_image_paths"}, inplace=True)
    
    for t in types:
        # Path of the full dataset images per class
        normal_full_path = os.path.join(data_folders_paths[t], "full", "normal" )
        abnormal_full_path = os.path.join(data_folders_paths[t], "full", "abnormal" )

        # Copy the testing images to appropriate folders (normal_test_path and abnormal_test_path)
        # Appropriate folders
        normal_test_path = os.path.join(data_folders_paths[t], "test", "normal" )
        abnormal_test_path = os.path.join(data_folders_paths[t], "test", "abnormal" )

        negative_test_image_paths = test_image_paths[test_image_paths['test_image_paths'].str.contains(t.upper()) & test_image_paths['test_image_paths'].str.contains("negative")]
        positive_test_image_paths = test_image_paths[test_image_paths['test_image_paths'].str.contains(t.upper()) & test_image_paths['test_image_paths'].str.contains("positive")]

        copy(negative_test_image_paths, normal_test_path)
        copy(positive_test_image_paths, abnormal_test_path)

        # Copy the testing images to the full dataset folder
        counter_full = copy_full(negative_test_image_paths, normal_full_path, counter_full)
        counter_full = copy_full(positive_test_image_paths, abnormal_full_path, counter_full)

        # Copy the training and validation images to appropriate folders (normal_train_path and abnormal_train_path, normal_val_path and abnormal_val_path)
        # Appropriate folders
        normal_train_path = os.path.join(data_folders_paths[t], "train", "normal" )
        abnormal_train_path = os.path.join(data_folders_paths[t], "train", "abnormal" )

        normal_val_path = os.path.join(data_folders_paths[t], "val", "normal" )
        abnormal_val_path = os.path.join(data_folders_paths[t], "val", "abnormal" )

        # Extract negative and positive images of type t from dataframe
        negative_trainval_image_paths = trainval_image_paths[trainval_image_paths['train_image_paths'].str.contains(t.upper()) & trainval_image_paths['train_image_paths'].str.contains("negative")]
        positive_trainval_image_paths = trainval_image_paths[trainval_image_paths['train_image_paths'].str.contains(t.upper()) & trainval_image_paths['train_image_paths'].str.contains("positive")]

        #Randomize images
        negative_trainval_image_paths = randomize(negative_trainval_image_paths)
        positive_trainval_image_paths = randomize(positive_trainval_image_paths)

        # In each type, select 15 % for validation
        number_negative_images = len(negative_trainval_image_paths)
        number_positive_images = len(positive_trainval_image_paths)

        number_val_negative_images = math.floor(0.15*number_negative_images)
        number_val_positive_images = math.floor(0.15*number_positive_images)

        # Divide dataframe in train and validation 
        train_negative_image_paths = negative_trainval_image_paths[0:(-number_val_negative_images)]
        train_positive_image_paths = positive_trainval_image_paths[0:(-number_val_positive_images)]
        val_negative_image_paths = negative_trainval_image_paths[(-number_val_negative_images):]
        val_positive_image_paths = positive_trainval_image_paths[(-number_val_positive_images):]

        # copy train images to train folder and val images to Validation folder, acording the images classes
        copy(train_negative_image_paths, normal_train_path)
        copy(train_positive_image_paths, abnormal_train_path)
        copy(val_negative_image_paths, normal_val_path)
        copy(val_positive_image_paths, abnormal_val_path)

        # copy train images to full dataset folder and val images to full dataset folder, acording the images classes
        counter_full = copy_full(train_negative_image_paths, normal_full_path, counter_full)
        counter_full = copy_full(train_positive_image_paths, abnormal_full_path, counter_full)
        counter_full = copy_full(val_negative_image_paths, normal_full_path, counter_full)
        counter_full = copy_full(val_positive_image_paths, abnormal_full_path, counter_full)
    print()
    print("'mura' dataset - Ready to be used in this Benchmark.")
    print()

if __name__ == "__main__":
    process_mura("./MURA-v1.1", "./mura")
