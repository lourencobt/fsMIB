# Dataset download and conversion

This file contains instructions to download the individual datasets used by fsMIB, and convert them into a common format (one TFRecord file per class). See [an overview](../README.md#downloading-and-converting-datasets) for
more context.

## covid

1.  Create a folder `covid`
2.  Inside `covid`, create a folder `COVID-QU-Ex-dataset`
3.  Download the zip file with the dataset from the
    [Covid-QU-Ex dataset](https://www.kaggle.com/datasets/anasmohammedtahir/covidqu) and save it as `COVID-QU-Ex-dataset.zip`
4.  Extract the zip content into `covid/COVID-QU-Ex-dataset`
5.  Copy `process_covid.py`  into `covid`
6.  Launch the conversion script:

    ```bash
    python3 process_covid.py
    ```

## breast
1.  Create a folder `breast`
2.  Inside `breast`, create a folder `Dataset_BUSI_with_GT`
3.  Download the zip file with the dataset from the
    [Breast Ultrasound Images](https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset) and save it as `Dataset_BUSI_with_GT.zip`
4. Extract the zip content into `breast/Dataset_BUSI_with_GT`
5. Copy `process_breast.py`, `delete_benign.csv` and `delete_malignant.csv` into `breast`
6. Launch the conversion script:

    ```bash
    python3 process_breast.py
    ```

**Note:** Since the original dataset was relatively small, I have manually identified the images that contained annotations on the position of the cancer. This images were collected in the `delete_benign.csv` and `delete_malignant.csv` files, in order to be removed from the final dataset.

**Examples:**

Benign examples:
<p float="center">
<img src="../figures/benign%20(14).png" height="150" />
<img src="../figures/benign%20(79).png" height="150" /> 
</p>

Malignant examples:
<p float="center">
<img src="../figures/malignant%20(2).png" height="150" />
<img src="../figures/malignant%20(10).png" height="150" /> 
</p>


## tuberculosis

1. Create a folder `tuberculosis`
2. Inside `tuberculosis`, create a folder `ChinaSet_AllFiles`
3. Download the zip file with the dataset from the [Shenzhen set](https://openi.nlm.nih.gov/faq#faq-tb-coll) in ”More Questions → Data Collection → I have heard about the Tuberculosis collection. Where can I get those images?”. Save it as `ChinaSet_AllFiles.zip`.
4. Extract the zip content into `tuberculosis/ChinaSet_AllFiles`
5. Copy `process_tuberculosis.py` into `tuberculosis`
6. Launch the conversion script:

    ```bash
    python3 process_tuberculosis.py
    ```

## skinlesion

1. Create a folder `skinlesion`
2. Access the [ISIC 2018](https://challenge.isic-archive.com/data/#2018) website. Then, download the data related to Task 3: 
   1. Training Data - Create `ISIC2018_Task3_Training_Input` folder
   2. Training Ground Truth - Create `ISIC2018_Task3_Training_GroundTruth` folder
   3. Validation Data - Create `ISIC2018_Task3_Validation_Input` folder
   4. Validation Ground Truth - Create `ISIC2018_Task3_Validation_GroundTruth` folder
3. Extract the 4 downloaded zip files corresponding to the above data into the corresponding folder
4. Copy `process_skinlesion.py` into `skinlesion`
5. Launch the conversion script:

    ```bash
    python3 process_skinlesion.py
    ```


## elbow / finger / forearm / hand / humerus / shoulder / wrist

1. Create a folder `MURA`
2. Access the [MURA](https://stanfordmlgroup.github.io/competitions/mura/) and fill the form to download the MURA dataset (v1.1)
3. Access the email you have received and download the zip file
4. Extract the zip content into `MURA/MURA-v1.1`
5. Copy `process_skinlesion.py`, `process_mura_preprocess.py` and `preProcess.py` into `MURA`
6. Launch one of the 2 conversion scripts:
    
    **Script that transforms the MURA dataset without pre-processing:**
    ```bash
    python3 process_mura.py
    ```
    
    **Script that transforms the MURA dataset with the pre-processing explained in [Mura Pre-processing Explained](../doc/mura_pre-processing.md):**
    ```bash
    python3 process_mura_preprocess.py
    ```
    **Note:** This script takes longer to complete
