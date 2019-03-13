#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 14:35:29 2019

@author: lg
"""
import os
import time
import shutil
from pathlib import Path

class S3cache():
    cache = None
    expiry = None #seconds
    
    def __init__(self,cache,expiry):
        '''Set cache expiry in seconds and path'''
        self.cache = Path(cache).resolve()
        self.expiry = expiry
        
    def cache_all(self,bucket,files):
        '''Download list of s3 files if not already in cache'''
        for f in files:
            self.cache_file(bucket,f.key)
          
        return None
    
    def cache_file(self,bucket,key):
        '''Download file from s3 if not already in cache'''
        if not self.cache_hit(key):
            dirs = key.split('/')[:-1]
            if dirs:
                dirs = Path('/'.join(dirs))
                if not os.path.isdir(self.cache / dirs):
                        os.makedirs(self.cache / dirs)      
                
            return bucket.download_file(key,str((self.cache / key).resolve()))
        
        return None
        
    def cache_hit(self,key):
        '''Check if file is in cache'''
        f = self.cache / key
     
        if  f.exists() and (os.path.getctime(f) - time.time()) <= self.expiry:
            return True
        else:
            return False

    def get_cache_file(self,key):
        '''Return file pointer to selected cached file'''
        if self.cache_hit(key):
            return open(self.cache / key,'rb')
        else:
            return None
        
    def delete_cache_file(self,key):
        '''Delete file in cache'''
        if self.cache_hit(key):
            os.remove(self.cache / key)
        
    def clean_cache(self):
        '''Delete all files in cache directory'''
        for d in os.listdir(self.cache):
            shutil.rmtree(self.cache / d)
    