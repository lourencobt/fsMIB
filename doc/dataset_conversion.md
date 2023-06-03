# Dataset download and conversion

This file contains instructions to download the individual datasets used by fsMIB and to convert them into a common format. See [an overview](../README.md#downloading-and-converting-datasets) for
more context.

Start by creating a folder `datasets`.

## covid

1.  Create a folder `covid` inside `datasets`
2.  Inside `covid`, create a folder `COVID-QU-Ex-dataset`
3.  Download the zip file with the dataset from the
    [Covid-QU-Ex dataset](https://www.kaggle.com/datasets/anasmohammedtahir/covidqu) and save it as `COVID-QU-Ex-dataset.zip`
4.  Extract the zip content into `covid/COVID-QU-Ex-dataset`
5.  Copy `convertion_scripts/covid/process_covid.py` into `covid`
6.  Launch the conversion script:

    ```bash
    python3 process_covid.py
    ```

## breast
1.  Create a folder `breast` inside `datasets`
2.  Inside `breast`, create a folder `Dataset_BUSI_with_GT`
3.  Download the zip file with the dataset from the
    [Breast Ultrasound Images](https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset) and save it as `Dataset_BUSI_with_GT.zip`
4. Extract the zip content into `breast/Dataset_BUSI_with_GT`
5. Copy `convertion_scripts/breast/process_breast.py`, `convertion_scripts/breast/delete_benign.csv` and `convertion_scripts/breast/delete_malignant.csv` into `breast`
6. Launch the conversion script:

    ```bash
    python3 process_breast.py
    ```

**Note:** Since the original dataset was relatively small, the images that contained annotations on the position of the cancer were manually identified and collected in the `delete_benign.csv` and `delete_malignant.csv` files, in order to be removed from the final dataset.

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

1. Create a folder `tuberculosis` inside `datasets`
2. Inside `tuberculosis`, create a folder `ChinaSet_AllFiles`
3. Download the zip file with the dataset from the [Shenzhen set](https://openi.nlm.nih.gov/faq#faq-tb-coll) in ”More Questions → Data Collection → I have heard about the Tuberculosis collection. Where can I get those images?”. Save it as `ChinaSet_AllFiles.zip`.
4. Extract the zip content into `tuberculosis/ChinaSet_AllFiles`
5. Copy `convertion_scripts/tuberculosis/process_tuberculosis.py` into `tuberculosis`
6. Launch the conversion script:

    ```bash
    python3 process_tuberculosis.py
    ```

## skinlesion

1. Create a folder `skinlesion` inside `datasets`
2. Access the [ISIC 2018](https://challenge.isic-archive.com/data/#2018) website. Then, download the data related to Task 3: 
   1. Training Data - Create `ISIC2018_Task3_Training_Input` folder
   2. Training Ground Truth - Create `ISIC2018_Task3_Training_GroundTruth` folder
   3. Validation Data - Create `ISIC2018_Task3_Validation_Input` folder
   4. Validation Ground Truth - Create `ISIC2018_Task3_Validation_GroundTruth` folder
3. Extract the 4 downloaded zip files corresponding to the above data into the corresponding folder
4. Copy `convertion_scripts/skinlesion/process_skinlesion.py` into `skinlesion`
5. Launch the conversion script:

    ```bash
    python3 process_skinlesion.py
    ```


## elbow / finger / forearm / hand / humerus / shoulder / wrist

1. Create a folder `MURA` inside `datasets`
2. Access the [MURA](https://stanfordmlgroup.github.io/competitions/mura/) and fill the form to download the MURA dataset (v1.1)
3. Access the email you have received and download the zip file
4. Extract the zip content into `MURA/MURA-v1.1`
5. Copy `convertion_scripts/MURA/process_mura.py`, `convertion_scripts/MURA/process_mura_preprocess.py` and `convertion_scripts/MURA/preProcess.py` into `MURA`
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

# Convert to tfrecords to use with Meta-Dataset reader
To use the Meta-Dataset code to create a reader for this datasets, it is necessary to convert the datasets into tensorflow records (tfrecords).

First, you need to clone the meta-dataset repository into the `datasets` folder and checkout to the version used in this work.

``` bash
    git clone https://github.com/google-research/meta-dataset.git
    
    cd meta-dataset

    git checkout 13ca9ed
```

Then, copy `adapted_code/pipeline.py` and `adapted_code/pipeline_medical.py` into `datasets/meta-dataset/meta_dataset/data/`. 

After that, copy `adapted_code/prepare_extra_datasets.py` into `datasets` folder and launch the script:

```bash
    python3 prepare_extra_datasets.py
```
**Note:** Do not forget to choose the value (True or False) of the **mura_processed** variable in the `prepare_extra_datasets.py`, according to the script chosen above.


This script will create a folder called `records` in each of the datasets (covid, breast, tuberculosis, skinlesion, elbow, finger, forearm, hand, humerus, shoulder, wrist), jointly with the corresponding json files that indicate the classes used in each of the splits. 

Differently from what happen with the [Meta-Dataset](https://github.com/google-research/meta-dataset), where the classes are divided in splits, in fsMIB the training, validation and test classes are always the same, because the medical imaging context has a limited amount of classes. To use the meta-dataset code, the datasets were divided creating, one dataset for each split. 

Finally, enter each of the `records` datasets folders and gather the `<dataset_name>_<split>` folders inside a new folder `datasets/records`. Gather also the `<dataset_name>_<split>_splits.json` in a new folder `datasets/splits`.