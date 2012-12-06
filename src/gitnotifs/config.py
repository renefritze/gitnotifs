'''
Created on Dec 6, 2012

@author: r_milk01
'''
from configparser import (SafeConfigParser as ConfigParser, NoOptionError,
                          ExtendedInterpolation)

class Config(ConfigParser):
    
    def __init__(self):
        super(Config, self).__init__(interpolation=ExtendedInterpolation())
    
    def __getitem__(self, key):
        section, key = key.split('.')
        return self.get(section, key)
