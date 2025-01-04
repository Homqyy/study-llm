#!/bin/bash

# download dataset for programming
modelscope download --dataset BAAI/IndustryCorpus2 --local_dir ./datasets/ include computer_programming_code/*
