#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：对于分类训练，整个数据集按照0.7的比例随机划分为训练集和测试集
"""
import os
import random
from shutil import copy2

train_dir = 'data/hxq_gj'
# train_dir = 'data/hxq_yf'

if not os.path.exists(train_dir + "_train"):
    os.mkdir(train_dir + "_train")
if not os.path.exists(train_dir + "_test"):
    os.mkdir(train_dir + "_test")

sub_dir = os.listdir(train_dir)
for dir in sub_dir:
    train_subdir = train_dir + "_train/" + dir
    test_subdir = train_dir + "_test/" + dir
    if not os.path.exists(train_subdir):
        os.mkdir(train_subdir)
    if not os.path.exists(test_subdir):
        os.mkdir(test_subdir)

    dir_files = os.listdir(os.path.join(train_dir, dir))
    num_files = len(dir_files)
    index_list = list(range(num_files))
    random.shuffle(index_list)
    num = 0
    for i in index_list:
        fileName = os.path.join(train_dir, dir, dir_files[i])
        if num < num_files * 0.7:
            copy2(fileName, train_subdir)
        else:
            copy2(fileName, test_subdir)
        num += 1