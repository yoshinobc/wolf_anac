from __future__ import print_function, division

import os
import sys

import numpy as np
import pandas as pd
import sklearn.linear_model
import math
import pickle

import aiwolfpy
import aiwolfpy.cash

import glob
predictor = aiwolfpy.cash.Predictor_5()
def game_data_filter(df, day, phase='daily_initialize', agent=0):


    y = np.zeros(60)
    # werewolves, possessed
    werewolves = []
    for i in range(1, 6):
        role = df["text"][i - 1].split()[2]
        if role == "WEREWOLF":
            werewolves.append(i)
        elif role == "POSSESSED":
            possessed = i

    for i in range(60):
        if predictor.case5.case60_df["agent_"+str(possessed)][i] == 2:
            if predictor.case5.case60_df["agent_"+str(werewolves[0])][i] ==1:
                y[i] = 1

    # role
    role = "VILLAGER"
    if agent > 0:
        role = df["text"][agent - 1].split()[2]

    # filter by role
    if role in ["VILLAGER", "POSSESSED"]:
        df = df[df["type"].isin(["talk", "vote", "execute", "dead"])]
    elif role == "MEDIUM":
        df = df[df["type"].isin(["talk", "vote", "execute", "dead", "identify"])]
    elif role == "SEER":
        df = df[df["type"].isin(["talk", "vote", "execute", "dead", "divine"])]
    elif role == "BODYGUARD":
        df = df[df["type"].isin(["talk", "vote", "execute", "dead", "guard"])]
    elif role == "WEREWOLF":
        df = df[df["type"].isin(["talk", "vote", "execute", "dead", "whisper", "attack", "attack_vote"])]


    # agent
    if agent == 0:
        agent = 1

        # filter by time
    if phase == 'daily_initialize':
        df = df[df["day"] < day]
    else:
        df = df[(df["day"] < day) | ((df["day"] == day) & (df["type"] == 'talk'))]

    predictor.initialize({"agent":agent, "roleMap":{str(agent):role},"agentIdx":agent}, {})
    predictor.update_features(df.reset_index())
    predictor.update_df()

    return predictor.df_pred, y

count = 0

model = sklearn.linear_model.LogisticRegression()
#wf = open("/home/AIWolfPy/train/train-log2.txt",mode="a")
dir_lists = glob.glob("/home/AIWolfPy/pre_logs/gat2017_05/*")
print(dir_lists)
#for k in range(1,1000):
for d in dir_lists:
    x_1000 = np.zeros((60000,80))
    y_1000 = np.zeros(60000)
    ind = 0
    file_lists = glob.glob(d+"/*")
    print(file_lists)
    #for i in range(100):
    for f in file_lists:
        #log_path = "/home/AIWolfPy/pre_logs/cedec_15/"+ "{0:03d}".format(k) + "/" + "{0:03d}".format(i) + ".log"
        log_path = f
        for d in range(3):
            try:
                text_ = aiwolfpy.read_log(log_path)
            except:
                continue
            x, y = game_data_filter(text_, day=d, phase='vote')
            x_1000[(ind*60):((ind+1)*60), :] = x
            y_1000[(ind*60):((ind+1)*60)] = y
            ind += 1
            x, y = game_data_filter(text_, day=d+1, phase='daily_initialize')
            x_1000[(ind*60):((ind+1)*60), :] = x
            y_1000[(ind*60):((ind+1)*60)] = y
            ind += 1
        model.fit(x_1000, y_1000)
        text = "epoch :" + str(count) + " score :" + str(model.score(x_1000,y_1000))
        print(text)
        wf = open("/home/AIWolfPy/train_gat5/train-log.txt",mode="a")
        wf.write(text)
        wf.write("\n")
        wf.close()
        count+=1
        if count%1000==0:
            filename = "/home/AIWolfPy/train_gat5/trainning_model-" + str(count) + ".sav"
            pickle.dump(model,open(filename,mode='wb'))
