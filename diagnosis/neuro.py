import csv
import numpy as np
import pandas as pd
import sklearn
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
pd.options.mode.chained_assignment = None
def predicate(features,model):
    features = np.array(features).reshape(1,-1)
    features = features.astype(np.float64)
    pred = model.predict(features)
    return pred