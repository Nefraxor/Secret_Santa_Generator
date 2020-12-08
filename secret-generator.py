#!/bin/python3

import pandas as pd
from random import randrange
from shutil import copyfile
import os

CWD = os.getcwd()
CSVPATH = CWD + "/results.csv"
BACKUPFILE = CWD + "/backup/tmp_backup.csv"
OUTPUTPATH = CWD + "/output/"

current_year=input('What year is it? (20XX)\r\n')

def secret_santa_generator():
    copyfile(CSVPATH, BACKUPFILE)

    df = pd.read_csv(CSVPATH, index_col=0) 
    names = df.index.values.tolist()
    givers = df.index.values.tolist()
    receivers = df.index.values.tolist()
        
    current_length = len(givers) 

    results = [None] * len(givers)

    giver_i = randrange(current_length)
    giver = givers[giver_i]
    first = giver

    while (current_length != 1):
        receiver_i = randrange(current_length)
        receiver = receivers[receiver_i]

        while (receiver == giver or not results[names.index(receiver)] is None or receiver in df.loc[giver].values):
            receiver_i = randrange(current_length)
            receiver = receivers[receiver_i]

        results[giver_i] = receiver

        giver_i = names.index(receiver)
        giver = givers[giver_i]

        current_length -= 1

        receivers.pop(receiver_i)

    results[giver_i] = first

    if (current_year in df.columns.values):
        if (input(f'Do you want to override year {current_year}? (y/n)\r\n') == 'y'):
            print('Overriding...')
        else:
            print('Exiting program')
            return

    df[current_year] = results

    df.to_csv(CSVPATH)

    for name in names:
        with open(f'{OUTPUTPATH}{name}_{current_year}.txt', "w") as f:
            f.write(results[names.index(name)])

secret_santa_generator()
