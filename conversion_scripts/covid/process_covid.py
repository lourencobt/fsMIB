import shutil
import os

def process_covid(src_path, dst_path):
    # Remove ".DS_Store" folder 
    for (root,dirs,files) in os.walk(src_path):
        for file in files:
            if ".DS_Store" in file:
                os.remove(os.path.join(root, file))

    # Remove the previous covid folder
    if os.path.exists(dst_path):
        remove = input(f"Removing '{os.path.abspath(dst_path)}', because it already exists. Are you sure of it? (Y or N) ")
        if remove.upper() == "Y" :
            shutil.rmtree(dst_path)
        elif remove.upper() == "N":
            exit()
        else:
            raise Exception("Invalid Answer")

    # Copy Lung Segmentation Data folder to the destination folder
    src_data_path = os.path.join(src_path, "Lung Segmentation Data")
    shutil.copytree(src_data_path, dst_path)

    # Rename Lung Segmentation Data to just `data``
    dst_data_path = os.path.join(dst_path, "Lung Segmentation Data")
    dst_data_path_final = os.path.join(dst_path, "data")
    os.rename(dst_data_path, dst_data_path_final)

    #Rename train, val and test folders - that were in the previously named `Lung Segmentation Data` folder - to lowercase
    train_folder_path = os.path.join(dst_path, "data/Train")
    train_folder_path_final = os.path.join(dst_path, "data/train")
    val_folder_path = os.path.join(dst_path, "data/Val")
    val_folder_path_final = os.path.join(dst_path, "data/val")
    test_folder_path = os.path.join(dst_path, "data/Test")
    test_folder_path_final = os.path.join(dst_path, "data/test")
    full_folder_path = os.path.join(dst_path, "data/full")
    os.rename(train_folder_path, train_folder_path_final)
    os.rename(val_folder_path, val_folder_path_final)
    os.rename(test_folder_path, test_folder_path_final)
    
    # Put images in class folder and Remove Images folder 
    for (root,dirs,files) in os.walk(dst_data_path_final):
        # Remove the folders with Segmentation Masks present in the previous folders
        # because they are not needed
        if "masks" in root:
            shutil.rmtree(root)
        
        # Copy the content of the `images` folder present in each `train`, `val` and `test` folders into the class folder 
        if "images" in root:
            for file in files:
                file_path = os.path.join(root, file)
                new_file_path = os.path.split(root)[0]
                shutil.move(file_path, new_file_path)

            # delete `images` folder
            shutil.rmtree(root)
    
    # Tupple with the name of the classes present in the covid dataset
    cls = ("COVID-19", "Non-COVID", "Normal")

    # path to the train, val and test folders
    splits_folders = (train_folder_path_final, val_folder_path_final, test_folder_path_final)

    # Create a `full` folder with one sub-folder per class. The full folder contains, per class, the images available in that class

    # Create the full
    os.mkdir(full_folder_path)

    for c in cls:
        # Create the sub-folders per class
        c_full_folder_path = os.path.join(full_folder_path, c)
        os.mkdir(c_full_folder_path)

        # Copy the images of each class in each partition to the correspondent subfolder 
        for split_path in splits_folders:
            path = os.path.join(split_path, c)
            
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                shutil.copy(file_path, c_full_folder_path)

    # Copy the "COVID-QU-Ex dataset.txt" file into the new dataset folder to maintain the information about the origin of this dataset
    info_path = os.path.join(src_path, "COVID-QU-Ex dataset.txt")
    shutil.copy(info_path, dst_path)

    print()
    print("'covid' dataset - Ready to be used in this Benchmark.")
    print()
    print("NOTE:")
    print("Be careful because the 'COVID-QU-Ex dataset.txt' file is from the original dataset. However, we maintained it for credits.")
    print()

if __name__ == "__main__":
    process_covid("./COVID-QU-Ex-dataset", "./covid")
