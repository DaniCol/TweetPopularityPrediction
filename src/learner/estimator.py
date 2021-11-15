import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor

class Estimator:
    def __init__(self, key, value, batch_size = 5):
        self.key = key
        self.data = pd.DataFrame(
            data={
                'beta': [value['X'][0]],
                'n_star': [value['X'][1]],
                'G1': [value['X'][2]],
                'W': value['W']
                }
            )
        self.estimator = RandomForestRegressor()
        self.batch_size = batch_size
        self.iterator_update = 0
    
    def push_back(self, value):
        self.data = self.data.append(
                            other={
                                'beta': value['X'][0],
                                'n_star': value['X'][1],
                                'G1': value['X'][2],
                                'W': value['W']
                            }, 
                            ignore_index=True)
    
    def fit(self):
        self.estimator.fit(
            X=self.data[['beta', 'n_star', 'G1']].to_numpy(), 
            y=self.data['W'].to_numpy())
    
    def handle(self, msg):
        # Add the new msg
        self.push_back(value=msg)
        self.iterator_update += 1

        # Do we fit the model
        if self.iterator_update == self.batch_size:
            self.iterator_update = 0
            self.fit()
            return True
        
        return False
