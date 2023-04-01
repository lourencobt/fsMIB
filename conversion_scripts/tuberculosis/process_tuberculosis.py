import math
import shutil
import os
import random

import numpy as np

def process_tuberculosis(src_path, dst_path):
    # Remove ".DS_Store" folder 
    for (root,dirs,files) in os.walk(src_path):
        for file in files:
            if ".DS_Store" in file:
                os.remove(os.path.join(root, file))

    # Remove the previous tuberculosis folder            
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
    classes = ("normal", "abnormal")
    
    # Create tuberculosis folder (Folder of the processed dataset)
    os.mkdir(dst_path)

    # Create data folder
    data_path = os.path.join(dst_path, "data")
    os.mkdir(data_path)

    # Create all the split folders in the tuberculosis dataset folder
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

    # In original dataset, "Image file names are coded as CHNCXR_#####_0/1.png, where ‘0’ represents the normal and ‘1’ represents the abnormal lung."
    # Walk in original dataset and save the path to the normal images to normal list and the abnormal ones to abnormal list
    orig_images_folder = os.path.join(src_path, "CXR_png")
    cls_image_paths = {}
    for cls in classes:
        cls_image_paths[cls] = []

    for file in os.listdir(orig_images_folder):
        if "0.png" in file:
            orig_file_path = os.path.join(orig_images_folder, file)
            cls_image_paths["normal"].append(orig_file_path)
        elif "1.png" in file:
            orig_file_path = os.path.join(orig_images_folder, file)
            cls_image_paths["abnormal"].append(orig_file_path)
    
    # Split the images in train, val and test partitions
    for cls in classes:
        # Shuffle the list with the image_paths
        random.shuffle(cls_image_paths[cls])

        # Split the images paths in train, val and test according to a rule of 70% / 15% / 15%
        train, val, test = np.split(cls_image_paths[cls], [int(len(cls_image_paths[cls])*0.7), int(len(cls_image_paths[cls])*0.85)])

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

    # Copy the "NLM-ChinaCXRSet-ReadMe.docx" file into the new dataset folder to maintain the information about the origin of this dataset
    info_path = os.path.join(src_path, "NLM-ChinaCXRSet-ReadMe.docx")
    shutil.copy(info_path, dst_path)

    print()
    print("'tuberculosis' dataset - Ready to be used in this Benchmark.")
    print()
    print("NOTE:")
    print("Be careful because the 'NLM-ChinaCXRSet-ReadMe.docx' file is from the original dataset. However, we maintained it for credits.")
    print()

if __name__ == "__main__":
    process_tuberculosis("./ChinaSet_AllFiles", "./tuberculosis")
