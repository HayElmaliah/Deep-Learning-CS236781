import math
import numpy as np
import torch
import torch.utils.data
from typing import Sized, Iterator
from torch.utils.data import Dataset, Sampler


class FirstLastSampler(Sampler):
    """
    A sampler that returns elements in a first-last order.
    """

    def __init__(self, data_source: Sized):
        """
        :param data_source: Source of data, can be anything that has a len(),
        since we only care about its number of elements.
        """
        super().__init__(data_source)
        self.data_source = data_source

    def __iter__(self) -> Iterator[int]:
        # Implement the logic required for this sampler.
        # If the length of the data source is N, you should return indices in a
        # first-last ordering, i.e. [0, N-1, 1, N-2, ...].
        # ====== YOUR CODE: ======
        for i in range(len(self.data_source)):
            if i > len(self.data_source) - 1 - i:
                break
            yield i
            if i == len(self.data_source) - 1 - i:
                break
            yield len(self.data_source) - 1 - i
        # ========================

    def __len__(self):
        return len(self.data_source)


def create_train_validation_loaders(
    dataset: Dataset, validation_ratio, batch_size=100, num_workers=2
):
    """
    Splits a dataset into a train and validation set, returning a
    DataLoader for each.
    :param dataset: The dataset to split.
    :param validation_ratio: Ratio (in range 0,1) of the validation set size to
        total dataset size.
    :param batch_size: Batch size the loaders will return from each set.
    :param num_workers: Number of workers to pass to dataloader init.
    :return: A tuple of train and validation DataLoader instances.
    """

    if not (0.0 < validation_ratio < 1.0):
        raise ValueError(validation_ratio)
    #  Create two DataLoader instances, dl_train and dl_valid.
    #  They should together represent a train/validation split of the given
    #  dataset. Make sure that:
    #  1. Validation set size is validation_ratio * total number of samples.
    #  2. No sample is in both datasets. You can select samples at random
    #     from the dataset.
    #  Hint: you can specify a Sampler class for the `DataLoader` instance
    #  you create.
    # ====== YOUR CODE: ======
    val_size = int(validation_ratio * len(dataset))
    indices = torch.randperm(len(dataset))
    train_sampler = torch.utils.data.SubsetRandomSampler(indices[val_size :])
    valid_sampler = torch.utils.data.SubsetRandomSampler(indices[:val_size])
    dl_train = torch.utils.data.DataLoader(
        dataset=dataset,
        sampler= train_sampler,
        batch_size=batch_size,
        num_workers=2)
    dl_valid =  torch.utils.data.DataLoader(
        dataset=dataset,
        sampler= valid_sampler,
        batch_size=batch_size,
        num_workers=2)
    return dl_train, dl_valid
    # ========================