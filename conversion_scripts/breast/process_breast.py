import shutil
import os
import random
import numpy as np
import pandas as pd

def process_breast(src_path, dst_path):
    # Remove ".DS_Store" folder 
    for (root,dirs,files) in os.walk(src_path):
        for file in files:
            if ".DS_Store" in file:
                os.remove(os.path.join(root, file))

    # Remove the previous breast folder
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
    # Tupple with the names of the classes in the breast dataset
    classes = ("benign", "malignant", "normal")

    # Create breast folder (Folder of the processed dataset)
    os.mkdir(dst_path)

    # Create data folder
    data_path = os.path.join(dst_path, "data")
    os.mkdir(data_path)

    # Create all the split folders in the breast dataset folder
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

    # Delete the images that contained annotations that indicate the position of the cancer in the image
    delete_benign = pd.read_csv('delete_benign.csv')
    delete_benign = [f"benign ({filenumber}).png" for filenumber in delete_benign["Number_of_file_to_delete"]]

    delete_malignant = pd.read_csv('delete_malignant.csv')
    delete_malignant = [f"malignant ({filenumber}).png" for filenumber in delete_malignant["Number_of_file_to_delete"]]

    for cls in classes:
        # construction of the full path to the images of each class. cls_image_paths is a list with all the paths to the images
        orig_cls_path = os.path.join(src_path, cls)
        if cls == "benign":
            files = [file for file in os.listdir(orig_cls_path) if file not in delete_benign]
        elif cls == "malignant":
            files = [file for file in os.listdir(orig_cls_path) if file not in delete_malignant]
        elif cls == "normal":
            files = [file for file in os.listdir(orig_cls_path)]
        cls_image_paths = [f"{orig_cls_path}/{file}" for file in files if ".png" in file and "mask" not in file ]

        # Shuffle the list with the image_paths
        random.shuffle(cls_image_paths)

        # Split the images paths in train, val and test according to a rule of 70% / 15% / 15%
        train, val, test = np.split(cls_image_paths, [int(len(cls_image_paths)*0.7), int(len(cls_image_paths)*0.85)])

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
    print("'breast' dataset - Ready to be used in this Benchmark.")
    print()

if __name__ == "__main__":
    process_breast("./Dataset_BUSI_with_GT","./breast")
