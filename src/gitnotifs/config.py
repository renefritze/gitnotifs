'''
Created on Dec 6, 2012

@author: r_milk01
'''
from ConfigParser import SafeConfigParser as ConfigParser

class Config(ConfigParser):
    
    def __getitem__(self, key):
        section, key = key.split('.')
        return self.get(section, key)
