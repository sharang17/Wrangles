#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Input: path to a file
Output: predicted house price
"""

import pandas as pd
import numpy as np
import pickle
import sys

def read_input(testDirPath):
    
    df = pd.read_csv(testDirPath)
    
    test_df =  df[['TOM', 'Crime', 'Restaurant', 'Education', 'Diversity']] 
    test_log_df = test_df.copy()
    cols = list(test_df.columns)
    for col in cols:
        test_log_df[col] = np.log(test_df[col])
        
    return test_log_df

    
def write_output(result):
    
    np.savetxt('price_output.out', result,  '%.2f', header= 'House Price')
    

def main():

    if len(sys.argv) > 1:
        testDirPath = sys.argv[1]
    else:
        print("Provide test data path.")
        testDirPath = '/home/leena/Documents/Projects/DSF/CSE519Project/price_input.csv'
    
    X_test = read_input(testDirPath)    
    
    try:
        price_model = load_model('/home/leena/Documents/Projects/DSF/CSE519Project/Baltimore_model.sav')
        prediction = (price_model.predict(X_test))
        
        result = np.exp(prediction)
        write_output(result)
        
    except:
        print('Something went wrong while loading pre trained model')
        
    
def save_model(filename, model):
    
    print("Saving model to disk.")
    pickle.dump(model, open(filename, 'wb'))
    
    
def load_model(filename='Baltimore_model.sav'):
    
    trained_model = pickle.load(open(filename, 'rb'))
    print("Pretrained model loaded.")
    return trained_model
    
    
if __name__ == '__main__':
	main()