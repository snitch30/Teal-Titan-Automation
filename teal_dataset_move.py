#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 09:34:28 2019

@author: stejasmunees
"""

import os
from shutil import copyfile
import shutil
import random
counter=0

source='/Users/stejasmunees/Desktop/TEAL/backup'
dest='/Users/stejasmunees/Desktop/TEAL/dat'

#source_dir=os.listdir(source)

#for folders in source_dir:
#    if folders[0]!='.':
#        for sub_folder in os.listdir(source+'/'+folders):
#            if sub_folder[0]!='.':
#                for files in os.listdir(source+'/'+folders+'/'+sub_folder):
#                    if files[0]!='.':
#                        counter+=1
#                        copyfile(source+'/'+folders+'/'+sub_folder+'/'+files, dest+'/'+sub_folder+'/'+files)

#yes_source='/Users/stejasmunees/Desktop/TEAL/dat_2/untitled folder/yes'
no_source='//Users/stejasmunees/Desktop/TEAL/dat_2/untitled folder/no'
#yes_source_dir=os.listdir(yes_source)
no_source_dir=os.listdir(no_source)
#yes_test_samples=random.sample(yes_source_dir, 400)
no_test_samples=random.sample(no_source_dir, 116)

no_dest='/Users/stejasmunees/Desktop/TEAL/dat_2/training_set/no'
#yes_dest='/Users/stejasmunees/Desktop/TEAL/dat_2/test_set/yes'
for no_files in no_test_samples:
    src=no_source+'/'+no_files
    dest=no_dest+'/'+no_files
    shutil.move(src,dest)
#for yes_files in yes_test_samples:
#    src=yes_source+'/'+yes_files
#    dest=yes_dest+'/'+yes_files
#    shutil.move(src,dest)


