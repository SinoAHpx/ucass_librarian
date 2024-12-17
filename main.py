# this is for executing the script

import sys
from config import read_config, write_default_config
from login import login
from reserve import *

conf = read_config()
if conf == None:
    print('An empty config was generated as there\'s none, please fill out information.')
    write_default_config()
    exit()
    
ic = login(conf.user.username, conf.user.password)

print(ic)