import pickle

import os
import sys

model = 'model_v2'

with open(f'../{model}.pkl', 'rb') as f:
        rf = pickle.load(f)


def make_prediction(input_data:list):
    new_variables = [input_data]
    return int(rf.predict(new_variables)[0])

# otro


# prueba1

