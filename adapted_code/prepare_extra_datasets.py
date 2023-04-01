# Adapted from CNAPS prepare_extra_datasets.py file used to deal with MNIST, CIFAR10, CIFAR100
# https://github.com/cambridge-mlg/cnaps/blob/master/src/prepare_extra_datasets.py
import os
import sys

os.environ['META_DATASET_ROOT'] = "./meta-dataset"
sys.path.append(os.path.abspath(os.environ['META_DATASET_ROOT']))
from meta_dataset.data import learning_spec
from meta_dataset.data import pipeline
from meta_dataset.data import dataset_spec as dataset_spec_lib
from meta_dataset.data import config
from meta_dataset.dataset_conversion.dataset_to_records import DatasetConverter, write_tfrecord_from_directory

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Quiet the TensorFlow warnings
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)  # Quiet the TensorFlow warnings

# True if mura was pre-processed, False if not
mura_preprocessed = True

class ExtraDatasetConverter(DatasetConverter):
    def __init__(self,
               name,
               data_root,
               split,
               has_superclasses=False,
               records_path=None,
               split_file=None,
               random_seed=22, 
               ) -> None:
        super().__init__(name, data_root, has_superclasses=has_superclasses, records_path = records_path, split_file=split_file, random_seed = random_seed)
        if split.lower() not in ("train", "val", "test"):
            raise Exception("In ExtraDatasetConverter Init, split must be: 'train', 'val', or 'test'")
        if split == "val":
            split = "valid"
        self.split = split.lower()

    def create_splits(self):
        if self.split == "train":
            class_names = sorted(os.listdir(self.data_root))
            return {'train': class_names, 'valid': [], 'test': []}
        elif self.split == "valid":
            class_names = sorted(os.listdir(self.data_root))
            return {'train': [], 'valid': class_names, 'test': []}
        elif self.split == "test":
            class_names = sorted(os.listdir(self.data_root))
            return {'train': [], 'valid': [], 'test': class_names}

    def create_dataset_specification_and_records(self):
        splits = self.get_splits(force_create=True)
        self.classes_per_split[learning_spec.Split.TRAIN] = len(splits['train'])
        self.classes_per_split[learning_spec.Split.VALID] = len(splits['valid'])
        self.classes_per_split[learning_spec.Split.TEST] = len(splits['test'])

        for class_id, class_name in enumerate(splits[self.split]):
            print('Creating record for class ID {} ({})'.format(class_id, class_name))
            class_directory = os.path.join(self.data_root, class_name)
            class_records_path = os.path.join(self.records_path, self.dataset_spec.file_pattern.format(class_id))
            self.class_names[class_id] = class_name
            self.images_per_class[class_id] = write_tfrecord_from_directory(class_directory, class_id, class_records_path)

def ExtraDatasetConverter_instantiation(dataset_root, dataset_name, split):
    if split.lower() not in ("train", "val", "test", "full"):
        raise Exception("In ExtraDatasetConverter_instantiation, split must be: 'train', 'val', 'test' or 'full'")

    print(f"SPLIT - {split}")
    if split == "full":
        dataset_name = dataset_name+"_"+split
        data_root = os.path.join(dataset_root, "data", split)
        split = "test"
    else:
        dataset_name = dataset_name+"_"+split
        data_root = os.path.join(dataset_root, "data", split)

    converter = ExtraDatasetConverter(
        name=dataset_name,
        data_root=data_root,
        split = split,
        has_superclasses=False,
        records_path=os.path.join(dataset_root, "records", dataset_name),
        split_file = os.path.join(dataset_root, dataset_name+"_splits.json"),
        random_seed=22
    )
    return converter

def main():
    
    COVID_ROOT = "./covid/covid"
    TUBERCULOSIS_ROOT = "./tuberculosis/tuberculosis"
    SKINLESION_ROOT = "./skinlesion/skinlesion"
    BREAST_ROOT = "./breast/breast"
    # MURA
    if mura_preprocessed == True:
        MURA_ROOT = "./MURA/mura_processed"
    else:
        MURA_ROOT = "./MURA/mura"
    MURA_TYPES = ('elbow', 'finger', 'forearm', 'hand', 'humerus', 'shoulder', 'wrist')

    dataset_names = ("covid", "breast", "tuberculosis", "skinlesion")
    splits = ("train", "val", "test", "full")
    ROOT = {
        "covid":  COVID_ROOT,
        "breast": BREAST_ROOT,
        "tuberculosis": TUBERCULOSIS_ROOT,
        "skinlesion": SKINLESION_ROOT
    }

    for type in MURA_TYPES:
        ROOT[type] = os.path.join(MURA_ROOT,type) 
    
    for dataset_name in dataset_names:
        for (root,dirs,files) in os.walk(ROOT[dataset_name]):
            for file in files:
                if ".DS_Store" in file:
                    os.remove(os.path.join(root, file))
        for split in splits:
            converter = ExtraDatasetConverter_instantiation(ROOT[dataset_name], dataset_name, split)
            converter.convert_dataset()
    
if __name__ == '__main__':
    main()

