# fsMIB
A **f**ew-**s**hot **M**edical **I**maging **B**enchmark (fsMIB): A dataset of datasets for learning to learn from few examples in the medical imaging domain. Based on the idea of Meta-Dataset.

# User Instructions
## Downloading and converting datasets 

fsMIB uses datasets that are public and available from different sources and in different formats. Below are the instructions to download and convert the datasets into a common format. 

### Dataset summary

Dataset (other names)                                                                                                                        | Number of classes  | Size on disk     | Converts into            
-------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------- | ---------------------------- | ---------------------------- 
[Covid-QU-Ex dataset](https://www.kaggle.com/datasets/anasmohammedtahir/covidqu)                                               | 3 | \~?? GiB | covid \[[instructions](doc/dataset_conversion.md#covid)\]                    
[Breast Ultrasound Images](https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset)                                                                    | 3 | \~?? GiB | breast  \[[instructions](doc/dataset_conversion.md#breast)\]                                        
[Shenzhen set](https://openi.nlm.nih.gov/faq#faq-tb-coll)                           | 2 | \~?? GiB | tuberculosis \[[instructions](doc/dataset_conversion.md#tuberculosis)\]                                                   
[ISIC 2018](https://challenge.isic-archive.com/data/#2018)                                     | 7 | \~?? GiB  | skinlesion \[[instructions](doc/dataset_conversion.md#skinlesion)\]   \
[MURA](https://stanfordmlgroup.github.io/competitions/mura/)   | 2 | \~?? GiB  | elbow / finger / forearm / hand / humerus / shoulder / wrist \[[instructions](doc/dataset_conversion.md#mura)\]                   
