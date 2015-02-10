import types
import numpy as np

dict_arr = {'a': 100, 'b':'boy', 'c':['o', 'p', 'q']}
arr = [1,2,3,4,5]
sub_arr = arr[0:2]

print sub_arr

for k in dict_arr:
    v = dict_arr.get(k)
    if type(v) is types.ListType: 
        print k, '---'
        for kk, vv in enumerate(v):
            print kk, vv
        print '---'
    else:
        print dict_arr.get(k)