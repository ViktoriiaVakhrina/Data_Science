import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder


class DataLoader(object):
    def fit(self, dataset):
        self.dataset=dataset.copy()

    def load_data(self):

        # remove column with 30% of '?' values: stalk-root
        self.dataset.drop('stalk-root', axis=1, inplace=True)

        # remove column with unique value: veil-type
        self.dataset.drop('veil-type', axis=1, inplace=True)

        # label encoding for all columns:

        le = LabelEncoder()
        cols = self.dataset.columns.tolist()
        for c in cols:
            le.fit(self.dataset[c])
            self.dataset[c] = le.transform(self.dataset[c])
        return self.dataset
