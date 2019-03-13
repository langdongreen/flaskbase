
"""
Created on Wed Jul  5 14:27:55 2017

@author: vulpi
"""
import json

def get_config(filename="config.json"):
    '''Read json formatted config file
    Paramaters: filename
    Return: configuration dictionary'''
    with open(filename) as json_data_file:
        return json.load(json_data_file)
        
def put_config(config,filename="config.json", ):
    '''Write json formatted configuration file
    Paramaters: filename, dictionary'''
    with open(filename, 'w') as outfile:
        json.dump(config, outfile,indent=4, sort_keys=True)
        
