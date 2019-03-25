#-*-coding:utf-8-*-
from __future__ import print_function
import torch.utils.data as data
from PIL import Image
import os
import sys
import pickle
import numpy as np
import lmdb
import torch
env = lmdb.open("/home/jn/code-pytorch/im2re-pytor-jn-NEW/im2recipe-Pytorch-master/data/test_lmdb", max_readers=1, readonly=True, lock=False, readahead=True, meminit=False)
txn = env.begin()
with open('/home/jn/code-pytorch/im2re-pytor-jn-NEW/im2recipe-Pytorch-master/data/test_keys.pkl', 'rb') as f:
    ids = pickle.load(f)
with env.begin(write=False) as txn:
    serialized_sample = txn.get(ids[5])
sample = pickle.loads(serialized_sample)
print(type(ids))
# print('len_imag',len(sample['imgs']))
# print(sample['classes'])
# print(sample)

keys = []
keys_class_count = {}
class_count = {}
num = int(len(ids) * 0.02)
for i in range(len(ids)):
    #print(i)
    with env.begin(write=False) as txn:
        serialized_sample = txn.get(ids[i])
        sample = pickle.loads(serialized_sample)
        if sample['classes'] not in class_count.keys():
            class_count[sample['classes']] = 1
        else:
            class_count[sample['classes']] = class_count[sample['classes']] + 1

# num = int(len(ids) * 0.02)
num = 500
print(class_count)

# num = int(class_count[sample['classes']]*0.02)

for i in range(len(ids)):
     #print(i)
     with env.begin(write=False) as txn:
         serialized_sample = txn.get(ids[i])
         sample = pickle.loads(serialized_sample)
     if sample['classes'] not in keys_class_count.keys():
         keys_class_count[sample['classes']] = 1

     if class_count[sample['classes']] > 2900:
         if keys_class_count[sample['classes']] <= 500:
             keys.append(ids[i])
             keys_class_count[sample['classes']] = keys_class_count[sample['classes']] + 1
     elif class_count[sample['classes']] < 2900 and class_count[sample['classes']] >= 500:
         if keys_class_count[sample['classes']] <= class_count[sample['classes']]*0.08:
             keys.append(ids[i])
             keys_class_count[sample['classes']] = keys_class_count[sample['classes']] + 1
     elif class_count[sample['classes']] < 500 and class_count[sample['classes']] >= 100:
         if keys_class_count[sample['classes']] <= class_count[sample['classes']]*0.06:
             keys.append(ids[i])
             keys_class_count[sample['classes']] = keys_class_count[sample['classes']] + 1
     elif class_count[sample['classes']] < 100 and class_count[sample['classes']] >= 30:
         if keys_class_count[sample['classes']] <= class_count[sample['classes']]*0.2:
             keys.append(ids[i])
             keys_class_count[sample['classes']] = keys_class_count[sample['classes']] + 1
     elif class_count[sample['classes']] < 30:
         if keys_class_count[sample['classes']] <= 30:
             keys.append(ids[i])
             keys_class_count[sample['classes']] = keys_class_count[sample['classes']] + 1
     # if keys_class_count[sample['classes']] <= num:
     #    keys.append(ids[i])
     #    keys_class_count[sample['classes']] = keys_class_count[sample['classes']] + 1

print(keys_class_count)
print(keys)
print(len(keys))


pickle.dump(keys,open("test_small_keys.pkl",'wb'))

# with open('/home/jn/code-pytorch/im2re-pytor-jn-NEW/im2recipe-Pytorch-master/num_pkl.pkl', 'rb') as f:
#      ids = pickle.load(f)
#
# print(ids)
# print(len(ids))


#for key, value in txn.cursor():
#    print(value)

#for i in ids:
 #   print(i)
# print(len(ids),ids[0])