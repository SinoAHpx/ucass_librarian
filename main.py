# this is for executing the script

import sys
from login import *
from reserve import *

args = sys.argv[1:]

#arg[0]: username, [1]: password, [2]: seat
if len(args) != 3:
    print(f'Please check your ares is proper: {args}')
    exit(-1)
    
#todo: save 'rememer me' cookie to reduce login

cookie = login(args[0], args[1])
if cookie == None:
    print(f'Login failed, check args: {args}')
    exit(-2)
    
print(f'Login successfully, cookie: {cookie}')

print(f'Start reserving: {args[2]}')