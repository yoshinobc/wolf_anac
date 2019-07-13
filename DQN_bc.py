# -*- coding:utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function, division

# this is main script
# simple version

import aiwolf_cp.aiwolfpy
import aiwolf_cp.aiwolfpy.contentbuilder as cb
from collections import deque
import numpy as np
import argparse
import sys
import signal
import os
import time
import pickle
import random
myname = 'dqn_bc'
import aiwolf_cp.aiwolfpy.ql
code = {"WEREWOLF":1,"VILLAGER":2,"SEER":3,"POSSESSED":4,"BODYGUARD":5,"MEDIUM":6,"ANY":7,"HUMAN":8,"SELF":9}
decode = {"1":"WEREWOLF","2":"VILLAGER","3":"SEER","4":"POSSESSED","5":"BODYGUARD","6":"MEDIUM","7":"ANY","8":"HUMAN","9":"SELF"}
thisRole = "VILLAGER"

def signal_handler(signal,frame):
    raise Exception("time out")

class SampleAgent(object):

    def __init__(self, agent_name):
        # myname
        self.altime = 0.5
        self.winlists = np.zeros(15)
        self.myname = agent_name
        self.load = False
        self.wolf_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",15)
        self.wolf_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",15)
        self.wolf_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",15)

        self.vill_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",15)
        self.vill_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",15)

        self.seer_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",15)
        self.seer_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",15)
        self.seer_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",15)
        self.seer_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",15)

        self.poss_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",15)
        self.poss_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",15)
        self.poss_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",15)

        self.guard_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",15)
        self.guard_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",15)
        self.guard_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",15)

        self.medi_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",15)
        self.medi_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",15)
        self.wolf_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",5)
        self.wolf_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",5)
        self.wolf_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",5)

        self.vill_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",5)
        self.vill_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",5)

        self.seer_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",5)
        self.seer_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",5)
        self.seer_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",5)
        self.seer_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",5)

        self.poss_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",5)
        self.poss_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",5)
        self.poss_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",5)
        """
        self.wolf_vote =aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",15)
        self.wolf_special =aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",15)
        self.wolf_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",15)
        self.wolf_vote2 =
        self.wolf_special2 =
        self.wolf_talk2 =


        self.vill_vote =aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",15)
        self.vill_talk =aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",15)
        self.vill_vote2 =
        self.vill_talk2 =

        self.seer_talk =aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",15)
        self.seer_vote =aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",15)
        self.seer_special =
        self.seer_talk_special =
        self.seer_talk2 =
        self.seer_vote2 =
        self.seer_special2 =
        self.seer_talk_special2 =


        self.poss_talk_special =
        self.poss_vote =
        self.poss_talk =
        self.poss_talk_special2 =
        self.poss_vote2 =
        self.poss_talk2 =


        self.guard_vote =
        self.guard_talk =
        self.guard_special =
        self.guard_vote2 =
        self.guard_talk2 =
        self.guard_special2 =


        self.medi_vote =
        self.medi_talk =
        self.medi_vote2 =
        self.medi_talk2 =
        """
    def getName(self):
        return self.myname
    """
    def signal_handler(signal,frame):
        raise Exception("time out")
    """

    def initialize(self, base_info, diff_data, game_setting):
        #print("Initialize")
        #self.log_file = open("after-log-"+ str(len(base_info["statusMap"])) + "-" + base_info["myRole"],"a")
        #start = time.time()
        #signal.signal(signal.SIGALRM,signal_handler)
        #signal.setitimer(signal.ITIMER_REAL,self.altime)
        self.playerNum = len(base_info["statusMap"])
        self.role = base_info["myRole"]
        print(self.load)
        if not self.load:
            print(self.playerNum)
            if self.playerNum == 15:
                self.wolf_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",15)
                self.wolf_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",15)
                self.wolf_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",15)

                self.vill_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",15)
                self.vill_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",15)

                self.seer_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",15)
                self.seer_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",15)
                self.seer_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",15)
                self.seer_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",15)

                self.poss_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",15)
                self.poss_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",15)
                self.poss_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",15)

                self.guard_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",15)
                self.guard_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",15)
                self.guard_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",15)

                self.medi_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",15)
                self.medi_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",15)
            else:
                print("test")
                self.wolf_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",5)
                self.wolf_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",5)
                self.wolf_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",5)

                self.vill_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",5)
                self.vill_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",5)

                self.seer_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",5)
                self.seer_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",5)
                self.seer_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",5)
                self.seer_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",5)

                self.poss_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",5)
                self.poss_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",5)
                self.poss_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",5)

            self.load = True
        if self.role == "VILLAGER":
            if self.playerNum == 15:
                self.dqn_vote = self.vill_vote
                self.dqn_talk = self.vill_talk
                self.dqn_special = None
                self.dqn_talk_special = None
            else:
                self.dqn_vote = self.vill_vote2
                self.dqn_talk = self.vill_talk2


        elif self.role == "WEREWOLF":
            if self.playerNum == 15:
                self.dqn_vote = self.wolf_vote
                self.dqn_special = self.wolf_special
                self.dqn_talk_special = None
                self.dqn_talk = self.wolf_talk
            else:
                self.dqn_vote = self.wolf_vote2
                self.dqn_special = self.wolf_special2
                self.dqn_talk = self.wolf_talk2

        elif self.role == "SEER":
            if self.playerNum == 15:
                self.dqn_vote = self.seer_vote
                self.dqn_talk = self.seer_talk
                self.dqn_special = self.seer_special
                self.dqn_talk_special = self.seer_talk_special
            else:
                self.dqn_vote = self.seer_vote2
                self.dqn_talk = self.seer_talk2
                self.dqn_special = self.seer_special2
                self.dqn_talk_special = self.seer_talk_special2

        elif self.role == "BODYGUARD":
            if self.playerNum == 15:
                self.dqn_vote = self.guard_vote
                self.dqn_talk = self.guard_talk
                self.dqn_special = self.guard_special
            else:
                self.dqn_vote = self.guard_vote2
                self.dqn_talk = self.guard_talk2
                self.dqn_special = self.guard_special2

        elif self.role == "POSSESSED":
            if self.playerNum == 15:
                self.dqn_vote = self.poss_vote
                self.dqn_talk = self.poss_talk
                self.dqn_special = None
                self.dqn_talk_special = self.poss_talk_special
            else:
                self.dqn_vote = self.poss_vote2
                self.dqn_talk = self.poss_talk2
                self.dqn_talk_special = self.poss_talk_special2

        elif self.role == "MEDIUM":
            if self.playerNum == 15:
                self.dqn_vote = self.medi_vote
                self.dqn_talk = self.medi_talk
                self.dqn_special = None
                self.dqn_talk_special = None
            else:
                self.dqn_vote = self.medi_vote2
                self.dqn_talk = self.medi_talk2
        self.base_info = base_info
        # game_setting
        self.talk_num = 0
        self.game_setting = game_setting
        #state=特殊能力:役職:CO, 投票:投票:生存, 疑う:特殊能力:自己, 投票済み

        self.stateCo = np.zeros((self.playerNum,self.playerNum))
        self.stateEs = np.zeros((self.playerNum,self.playerNum))
        self.stateVote = np.zeros((self.playerNum,self.playerNum))
        self.stateTalk = np.zeros((self.playerNum,self.playerNum))
        self.stateTalkNum = np.zeros(self.playerNum)
        self.stateIsAlive = np.zeros(self.playerNum)
        self.dayvote = np.zeros(self.playerNum)
        self.onedaycoseer = set()
        self.rpp = False
        self.day = -1

        self.index = base_info['agentIdx']

        self.finishCount = 0
        self.possiblewolf = []
        for i in range(self.playerNum):
            self.possiblewolf.append(True)
        self.islearn = True
        self.stateLog = []
        self.actionLog = []
        self.actionLog_vote = []
        self.stateLog_vote = []
        self.actionLog_special = []
        self.stateLog_special = []
        self.stateLog_talk = []
        self.actionLog_talk = []
        self.reward = 0
        self.wolflists = []
        self.wolfattacklists = np.zeros(self.playerNum)
        """
        try:
            self.playerNum = len(base_info["statusMap"])
            self.role = base_info["myRole"]
            print(self.role,self.playerNum)
            if not self.load:
                if self.playerNum == 15:
                    self.wolf_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",15)
                    self.wolf_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",15)
                    self.wolf_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",15)

                    self.vill_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",15)
                    self.vill_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",15)

                    self.seer_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",15)
                    self.seer_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",15)
                    self.seer_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",15)
                    self.seer_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",15)

                    self.poss_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",15)
                    self.poss_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",15)
                    self.poss_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",15)

                    self.guard_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",15)
                    self.guard_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",15)
                    self.guard_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",15)

                    self.medi_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",15)
                    self.medi_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",15)
                else:
                    print("test")
                    self.wolf_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",5)
                    self.wolf_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",5)
                    self.wolf_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",5)

                    self.vill_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",5)
                    self.vill_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",5)

                    self.seer_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",5)
                    self.seer_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",5)
                    self.seer_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",5)
                    self.seer_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",5)

                    self.poss_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",5)
                    self.poss_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",5)
                    self.poss_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",5)

                self.load = True
            if self.role == "VILLAGER":
                if self.playerNum == 15:
                    self.dqn_vote = self.vill_vote
                    self.dqn_talk = self.vill_talk
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = self.vill_vote2
                    self.dqn_talk = self.vill_talk2


            elif self.role == "WEREWOLF":
                if self.playerNum == 15:
                    self.dqn_vote = self.wolf_vote
                    self.dqn_special = self.wolf_special
                    self.dqn_talk_special = None
                    self.dqn_talk = self.wolf_talk
                else:
                    self.dqn_vote = self.wolf_vote2
                    self.dqn_special = self.wolf_special2
                    self.dqn_talk = self.wolf_talk2

            elif self.role == "SEER":
                if self.playerNum == 15:
                    self.dqn_vote = self.seer_vote
                    self.dqn_talk = self.seer_talk
                    self.dqn_special = self.seer_special
                    self.dqn_talk_special = self.seer_talk_special
                else:
                    self.dqn_vote = self.seer_vote2
                    self.dqn_talk = self.seer_talk2
                    self.dqn_special = self.seer_special2
                    self.dqn_talk_special = self.seer_talk_special2

            elif self.role == "BODYGUARD":
                if self.playerNum == 15:
                    self.dqn_vote = self.guard_vote
                    self.dqn_talk = self.guard_talk
                    self.dqn_special = self.guard_special
                else:
                    self.dqn_vote = self.guard_vote2
                    self.dqn_talk = self.guard_talk2
                    self.dqn_special = self.guard_special2

            elif self.role == "POSSESSED":
                if self.playerNum == 15:
                    self.dqn_vote = self.poss_vote
                    self.dqn_talk = self.poss_talk
                    self.dqn_special = None
                    self.dqn_talk_special = self.poss_talk_special
                else:
                    self.dqn_vote = self.poss_vote2
                    self.dqn_talk = self.poss_talk2
                    self.dqn_talk_special = self.poss_talk_special2

            elif self.role == "MEDIUM":
                if self.playerNum == 15:
                    self.dqn_vote = self.medi_vote
                    self.dqn_talk = self.medi_talk
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = self.medi_vote2
                    self.dqn_talk = self.medi_talk2


            if self.role == "VILLAGER":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",15)
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",5)


            elif self.role == "WEREWOLF":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",15)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",15)
                    self.dqn_talk_special = None
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",5)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",5)

            elif self.role == "SEER":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",15)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",15)
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",5)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",5)
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",5)

            elif self.role == "BODYGUARD":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",15)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",5)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",5)

            elif self.role == "POSSESSED":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",15)
                    self.dqn_special = None
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",5)
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",5)

            elif self.role == "MEDIUM":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",15)
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",5)


            self.base_info = base_info
            # game_setting
            self.talk_num = 0
            self.game_setting = game_setting
            #state=特殊能力:役職:CO, 投票:投票:生存, 疑う:特殊能力:自己, 投票済み

            self.stateCo = np.zeros((self.playerNum,self.playerNum))
            self.stateEs = np.zeros((self.playerNum,self.playerNum))
            self.stateVote = np.zeros((self.playerNum,self.playerNum))
            self.stateTalk = np.zeros((self.playerNum,self.playerNum))
            self.stateTalkNum = np.zeros(self.playerNum)
            self.stateIsAlive = np.zeros(self.playerNum)
            self.dayvote = np.zeros(self.playerNum)
            self.onedaycoseer = set()
            self.rpp = False
            self.day = -1

            self.index = base_info['agentIdx']

            self.finishCount = 0
            self.possiblewolf = []
            for i in range(self.playerNum):
                self.possiblewolf.append(True)
            self.islearn = True
            self.stateLog = []
            self.actionLog = []
            self.actionLog_vote = []
            self.stateLog_vote = []
            self.actionLog_special = []
            self.stateLog_special = []
            self.stateLog_talk = []
            self.actionLog_talk = []
            self.reward = 0
            self.wolflists = []
            self.wolfattacklists = np.zeros(self.playerNum)
            #text = "initialize," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
            signal.setitimer(signal.ITIMER_REAL,0)
        except Exception:
            signal.setitimer(signal.ITIMER_REAL,0)
            self.playerNum = len(base_info["statusMap"])
            self.role = base_info["myRole"]
            if not self.load:
                if self.playerNum == 15:
                    self.wolf_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",15)
                    self.wolf_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",15)
                    self.wolf_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",15)

                    self.vill_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",15)
                    self.vill_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",15)

                    self.seer_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",15)
                    self.seer_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",15)
                    self.seer_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",15)
                    self.seer_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",15)

                    self.poss_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",15)
                    self.poss_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",15)
                    self.poss_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",15)

                    self.guard_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",15)
                    self.guard_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",15)
                    self.guard_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",15)

                    self.medi_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",15)
                    self.medi_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",15)
                else:
                    self.wolf_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",5)
                    self.wolf_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",5)
                    self.wolf_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",5)

                    self.vill_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",5)
                    self.vill_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",5)

                    self.seer_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",5)
                    self.seer_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",5)
                    self.seer_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",5)
                    self.seer_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",5)

                    self.poss_talk_special2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",5)
                    self.poss_vote2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",5)
                    self.poss_talk2 = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",5)

                self.load = True
            if self.role == "VILLAGER":
                if self.playerNum == 15:
                    self.dqn_vote = self.vill_vote
                    self.dqn_talk = self.vill_talk
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = self.vill_vote2
                    self.dqn_talk = self.vill_talk2


            elif self.role == "WEREWOLF":
                if self.playerNum == 15:
                    self.dqn_vote = self.wolf_vote
                    self.dqn_special = self.wolf_special
                    self.dqn_talk_special = None
                    self.dqn_talk = self.wolf_talk
                else:
                    self.dqn_vote = self.wolf_vote2
                    self.dqn_special = self.wolf_special2
                    self.dqn_talk = self.wolf_talk2

            elif self.role == "SEER":
                if self.playerNum == 15:
                    self.dqn_vote = self.seer_vote
                    self.dqn_talk = self.seer_talk
                    self.dqn_special = self.seer_special
                    self.dqn_talk_special = self.seer_talk_special
                else:
                    self.dqn_vote = self.seer_vote2
                    self.dqn_talk = self.seer_talk2
                    self.dqn_special = self.seer_special2
                    self.dqn_talk_special = self.seer_talk_special2

            elif self.role == "BODYGUARD":
                if self.playerNum == 15:
                    self.dqn_vote = self.guard_vote
                    self.dqn_talk = self.guard_talk
                    self.dqn_special = self.guard_special
                else:
                    self.dqn_vote = self.guard_vote2
                    self.dqn_talk = self.guard_talk2
                    self.dqn_special = self.guard_special2

            elif self.role == "POSSESSED":
                if self.playerNum == 15:
                    self.dqn_vote = self.poss_vote
                    self.dqn_talk = self.poss_talk
                    self.dqn_special = None
                    self.dqn_talk_special = self.poss_talk_special
                else:
                    self.dqn_vote = self.poss_vote2
                    self.dqn_talk = self.poss_talk2
                    self.dqn_talk_special = self.poss_talk_special2

            elif self.role == "MEDIUM":
                if self.playerNum == 15:
                    self.dqn_vote = self.medi_vote
                    self.dqn_talk = self.medi_talk
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = self.medi_vote2
                    self.dqn_talk = self.medi_talk2


            if self.role == "VILLAGER":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",15)
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("VILLAGER","talk",5)


            elif self.role == "WEREWOLF":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",15)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",15)
                    self.dqn_talk_special = None
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","vote",5)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","special",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("WEREWOLF","talk",5)

            elif self.role == "SEER":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",15)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",15)
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk",5)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","special",5)
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("SEER","talk_special",5)

            elif self.role == "BODYGUARD":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",15)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","talk",5)
                    self.dqn_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("BODYGUARD","special",5)

            elif self.role == "POSSESSED":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",15)
                    self.dqn_special = None
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",15)
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk",5)
                    self.dqn_talk_special = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("POSSESSED","talk_special",5)

            elif self.role == "MEDIUM":
                if self.playerNum == 15:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",15)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",15)
                    self.dqn_special = None
                    self.dqn_talk_special = None
                else:
                    self.dqn_vote = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","vote",5)
                    self.dqn_talk = aiwolf_cp.aiwolfpy.ql.DeepQNetwork_bc("MEDIUM","talk",5)


            self.base_info = base_info
            # game_setting
            self.talk_num = 0
            self.game_setting = game_setting
            #state=特殊能力:役職:CO, 投票:投票:生存, 疑う:特殊能力:自己, 投票済み

            self.stateCo = np.zeros((self.playerNum,self.playerNum))
            self.stateEs = np.zeros((self.playerNum,self.playerNum))
            self.stateVote = np.zeros((self.playerNum,self.playerNum))
            self.stateTalk = np.zeros((self.playerNum,self.playerNum))
            self.stateTalkNum = np.zeros(self.playerNum)
            self.stateIsAlive = np.zeros(self.playerNum)
            self.dayvote = np.zeros(self.playerNum)
            self.onedaycoseer = set()
            self.rpp = False
            self.day = -1

            self.index = base_info['agentIdx']

            self.finishCount = 0
            self.possiblewolf = []
            for i in range(self.playerNum):
                self.possiblewolf.append(True)
            self.islearn = True
            self.stateLog = []
            self.actionLog = []
            self.actionLog_vote = []
            self.stateLog_vote = []
            self.actionLog_special = []
            self.stateLog_special = []
            self.stateLog_talk = []
            self.actionLog_talk = []
            self.reward = 0
            self.wolflists = []
            self.wolfattacklists = np.zeros(self.playerNum)
        """
    def update(self, base_info, diff_data, request):
        #print(self.day,"update")
        #print(diff_data)
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            start = time.time()
            self.base_info = base_info
            self.diff_data = diff_data
            self.statusMap = base_info["statusMap"]
            if len(diff_data) == 0 or not self.islearn:
                #print(self.day,"return")
                signal.setitimer(signal.ITIMER_REAL,0)
                return
            #print(diff_data,request)
            if diff_data["type"][0] == "finish":
                wolves,humans = [],[]
                colist = np.array([self.diff_data["text"]])
                for i in range(len(colist)):
                    content = self.splitText(colist[0][i])
                    if content[2] == "WEREWOLF" or content[2] == "POSSESSED":
                        wolves.append(int(content[1])-1)
                    else:
                        humans.append(int(content[1])-1)
                statusMap = self.base_info["statusMap"]
                alivelist = []
                is_vill_win = True
                for i in range(1,self.playerNum+1):
                    if(statusMap[str(i)] == "ALIVE"):
                        alivelist.append(i-1)
                for i in alivelist:
                    if i in wolves:
                        is_vill_win = False
                if(is_vill_win):
                    for i in humans:
                        self.winlists[i] += 1
                else:
                    for i in wolves:
                        self.winlists[i] += 1

            if diff_data["type"][0] == "whisper":
                #print("whisper")
                whisperlist = np.array([diff_data["agent"],diff_data["text"]])
                #print(whisperlist)
                for i in range(len(whisperlist)):
                    content = self.splitText(whisperlist[1][i])
                    if len(content) == 0:
                        continue
                    for j in range(len(whisperlist[0])):
                        self.possiblewolf[int(whisperlist[0][j])-1] = False
                        self.wolflists.append(int(whisperlist[0][j]-1))
                    if content[0] == "COMINGOUT":
                        if content[2] == "WEREWOLF":
                            #print(content[0],content[1],content[2])
                            self.possiblewolf[int(content[1])-1] = False

            if diff_data["type"][0] == "talk":
                #self.day = diff_data["day"][0] + 1
                talklist = np.array([diff_data["agent"],diff_data["text"]])
                for i in range(len(talklist[0])):
                    content = self.splitText(talklist[1][i])
                    if len(content) == 0:
                        continue
                    if content[0] == "COMINGOUT":
                        self.wolfvotezeroday[talklist[0][i]-1] = int(content[1])-1
                        self.stateCo[talklist[0][i]-1][int(content[1])-1] = code[content[2]]
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                        if content[2] == "SEER" and self.day == 1:
                            self.onedaycoseer.add(talklist[0][i])
                    elif content[0] == "ESTIMATE":
                        self.stateEs[talklist[0][i]-1][int(content[1])-1] = code[content[2]]
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "DIVINED":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "DIVINATION":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "GUARD":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "VOTE":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "ATTACK":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "DIVINED":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "IDENTIFIED":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "GUARDED":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "VOTED":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "ATTACKED":
                        self.stateTalk[talklist[0][i]-1][int(content[1])-1] += 1
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "AGREE":
                        self.stateTalkNum[talklist[0][i]-1] += 1
                    elif content[0] == "DISAGREE":
                        self.stateTalkNum[talklist[0][i]-1] += 1

            #stateVote

            #stateIsAlive
            self.dayvote = np.zeros(self.playerNum)
            for i in range(len(diff_data)):
                #print(diff_data["type"][i])
                if diff_data["type"][i] == "execute":
                    if self.stateIsAlive[diff_data["agent"][i]-1] == 0:
                        self.stateIsAlive[diff_data["agent"][i]-1] = 1 + self.day
                elif diff_data["type"][i] == "dead":
                    if self.stateIsAlive[diff_data["agent"][i]-1] == 0:
                        self.stateIsAlive[diff_data["agent"][i]-1] = 20 + self.day
                elif diff_data["type"][i] == "vote":
                    if diff_data["agent"][i]-1 in self.wolflists:
                        self.wolfattacklists[diff_data["idx"][i]-1] += 1
                    self.stateVote[diff_data["idx"][i]-1][diff_data["agent"][i]-1] +=1
                    self.dayvote[diff_data["agent"][i]-1] += 1
                elif diff_data["type"][i] == "identify":
                    self.identifiedIdx = {}
                    content = self.splitText(diff_data["text"][i])
                    self.identifiedIdx[content[1]-1] = content[2]
                elif diff_data["type"][i] == "divine":
                    self.divineIdx = {}
                    content = self.splitText(diff_data["text"][i])
                    self.divineIdx[content[1]-1] = content[2]
            #text = "initialize," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
        except Exception:
            print("333timeout")
            signal.setitimer(signal.ITIMER_REAL,0)

    def attack(self):
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            if self.day == 0:
                #print("307")
                self.attackIdx = np.argmax(self.winlists)+1
                #text = "attack0," + str(time.time()-start) + "\n"
                #self.log_file.write(text)
                signal.setitimer(signal.ITIMER_REAL,0)
                return self.attackIdx
            elif self.day != 0:
                possibleActions = self.possible()
                state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                state = np.concatenate(([self.day],state))
                state = np.concatenate(([code[self.role]],state))
                #print(self.stateLog_special)

                action_index = self.dqn_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                self.stateLog_special.append(state)
                    #print(log_action)
                actions = self.onehot(action_index-1,self.playerNum)
                self.actionLog_special.append(actions)
                self.attackIdx = action_index
                #text = "attack1," + str(time.time()-start) + "\n"
                #self.log_file.write(text)
                signal.setitimer(signal.ITIMER_REAL,0)
                return action_index
        except Exception:
            print("355timeout")
            signal.setitimer(signal.ITIMER_REAL,0)
            return random.randint(1,self.playerNum)

    def divine(self):
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            possibleActions = self.possible()
            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
            state = np.concatenate(([self.day],state))
            state = np.concatenate(([code[self.role]],state))
            #print(self.stateLog_special)

            action_index = self.dqn_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
            self.stateLog_special.append(state)
            #print(log_action)
            actions = self.onehot(action_index-1,self.playerNum)
            self.actionLog_special.append(actions)
            #text = "divine," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
            signal.setitimer(signal.ITIMER_REAL,0)
            return action_index
        except Exception:
            print("384timeout")
            signal.setitimer(signal.ITIMER_REAL,0)
            return random.randint(1,self.playerNum)


    def vote(self):
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            if self.role == "VILLAGER" and self.playerNum == 5 and self.rpp:
                for i in range(1,6):
                    if i-1 not in self.onedaycoseer and i-1 != self.base_info["agentIdx"]:
                        signal.setitimer(signal.ITIMER_REAL,0)
                        return i
            possibleActions = self.possible()
            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
            state = np.concatenate(([self.day],state))
            state = np.concatenate(([code[self.role]],state))
            #print(self.stateLog_special)

            action_index = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
            self.stateLog_vote.append(state)
            #print(log_action)
            actions = self.onehot(action_index-1,self.playerNum)
            self.actionLog_vote.append(actions)
            #text = "vote," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
            signal.setitimer(signal.ITIMER_REAL,0)
            return action_index
        except Exception:
            print("414timeout")
            signal.setitimer(signal.ITIMER_REAL,0)
            return random.randint(1,self.playerNum)

    def guard(self):
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            possibleActions = self.possible()
            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
            state = np.concatenate(([self.day],state))
            state = np.concatenate(([code[self.role]],state))
            #print(self.stateLog_special)

            action_index = self.dqn_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
            self.stateLog_special.append(state)
            #print(log_action)
            actions = self.onehot(action_index-1,self.playerNum)
            self.actionLog_special.append(actions)
            #text = "guard," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
            signal.setitimer(signal.ITIMER_REAL,0)
            return action_index
        except Exception:
            print("443timeout")
            signal.setitimer(signal.ITIMER_REAL,0)
            return random.randint(1,self.playerNum)

    def dayStart(self):
        #print("dayStart")
        #print("dayStart")
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            start = time.time()
            self.talk_count = 0
            self.whisper_count = 0
            self.action_flag = False
            self.action = None
            self.voteaction = None
            self.day += 1
            self.wolfvotezeroday = {}
            #text = "dayStart," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
            signal.setitimer(signal.ITIMER_REAL,0)
            return None
        except Exception:
            print("443timeout")
            signal.setitimer(signal.ITIMER_REAL,0)
            return None

    def whisper(self):
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            if self.day == 0 and self.whisper_count == 0:
                self.whisper_count += 1
                signal.setitimer(signal.ITIMER_REAL,0)
                return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
            elif self.day == 0 and self.whisper_count == 1:
                self.whisper_count += 1
                signal.setitimer(signal.ITIMER_REAL,0)
                return cb.attack(np.argmax(self.winlists)+1)
            elif self.day == 0 and self.whisper_count == 2:
                self.whisper_count += 1
                signal.setitimer(signal.ITIMER_REAL,0)
                return cb.comingout(self.base_info["agentIdx"],"WEREWOLF")
            elif self.day != 0 and self.whisper_count == 0:
                self.whisper_count += 1
                signal.setitimer(signal.ITIMER_REAL,0)
                return cb.attack(np.argmax(self.wolfattacklists)+1)
            #text = "whisper," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
            signal.setitimer(signal.ITIMER_REAL,0)
            return cb.skip()
        except Exception:
            print("487timeout")
            signal.setitimer(signal.ITIMER_REAL,0)
            return cb.skip()

    def talk(self):
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            #print(self.playerNum,self.role)
            if self.playerNum == 5:
                #print("test")
                if self.role == "VILLAGER" :
                    if self.day == 0:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "vi-0-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)

                            return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            #text = "vi-0-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(np.argmax(self.winlists)+1)
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "vi-0-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                    else:
                        if self.talk_count  == 0:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)
                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "vi-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                        elif self.talk_count <= 10:
                            if len(self.onedaycoseer) == 2:
                                for k in self.onedaycoseer:
                                    if self.base_info["statusMap"][str(k+1)] == "ALIVE":
                                        self.rpp = True
                                if self.rpp:
                                    self.talk_count += 20
                                    signal.setitimer(signal.ITIMER_REAL,0)
                                    return cb.comingout(self.base_info["agentIdx"],"WEREWOLF")


                elif self.role == "WEREWOLF":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "we-0-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            #text = "we-0-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return  cb.vote(np.argmax(self.winlists)+1)
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "we-0-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                    else:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "we-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                elif self.role == "SEER":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"SEER")
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(np.argmax(self.winlists)+1)
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                    else:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                        elif self.talk_count == 1:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk_special.get_talk(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(action_index,"WEREWOLF")

                elif self.role == "POSSESSED":
                    print(self.day,self.talk_count,5)
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"SEER")
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(np.argmax(self.winlists)+1)
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                else:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        possibleActions = self.possible()
                        state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                        state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                        state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                        state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                        state = np.concatenate(([self.day],state))
                        state = np.concatenate(([code[self.role]],state))
                        #print(self.stateLog_special)

                        action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        self.stateLog.append(state)
                        #print(log_action)
                        actions = self.onehot(action_index-1,self.playerNum)
                        self.actionLog.append(actions)
                        signal.setitimer(signal.ITIMER_REAL,0)
                        return cb.vote(action_index)

                    elif self.talk_count == 1:
                        self.talk_count += 1
                        possibleActions = self.possible()
                        state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                        state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                        state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                        state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                        state = np.concatenate(([self.day],state))
                        state = np.concatenate(([code[self.role]],state))
                        #print(self.stateLog_special)

                        action_index = self.dqn_talk_special.get_talk(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        self.stateLog.append(state)
                        actions = self.onehot(action_index-1,self.playerNum)
                        self.actionLog.append(actions)
                        signal.setitimer(signal.ITIMER_REAL,0)
                        return cb.comingout(action_index,"WEREWOLF")

            else:
                if self.role == "VILLAGER":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "vi-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(np.argmax(self.winlists)+1)
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            #text = "vi-1-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "vi-1-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                    else:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)


                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "vi-2-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                elif self.role == "SEER":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "se-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"SEER")
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            #text = "se-1-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.divined(list(self.divineIdx.keys())[0],list(self.divineIdx.values())[0])
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "se-1-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                    else:
                        if self.talk_count == 0:
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index,role_index = self.dqn_talk_special.get_talk(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            actions = self.onehot(action_index-1,self.playerNum)
                            roles = self.onehot(role_index-1,6)
                            self.actionLog.append(np.concatenate((actions,roles)))
                            #text = "se-2-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return "DIVINED AGENT[" + str(action_index) + "] " + str(decode[str(int(role_index))])

                        elif self.talk_count == 1:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "se-2-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                elif self.role == "MEDIUM":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "me-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"MEDIUM")
                    else:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "me-1-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.identified(list(self.identifiedIdx.keys())[0],list(self.identifiedIdx.values())[0])
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "me-1-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                elif self.role == "BODYGUARD":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "bo-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(np.argmax(self.winlists)+1)
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            #text = "bo-1-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "bo-1-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                    else:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "bo-1-3," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                elif self.role == "WEREWOLF":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "we-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            #text = "we-1-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(np.argmax(self.winlists)+1)
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "we-1-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                    else:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            if len(list(self.wolfvotezeroday.values())) >= 1:
                                #text = "we-2-0," + str(time.time()-start) + "\n"
                                #self.log_file.write(text)
                                signal.setitimer(signal.ITIMER_REAL,0)
                                return cb.vote(list(self.wolfvotezeroday.values())[0])
                            else:
                                possibleActions = self.possible()
                                state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                                state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                                state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                                state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                                state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                                state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                                state = np.concatenate(([self.day],state))
                                state = np.concatenate(([code[self.role]],state))
                                #print(self.stateLog_special)

                                action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                                self.stateLog.append(state)
                                #print(log_action)
                                actions = self.onehot(action_index-1,self.playerNum)
                                self.actionLog.append(actions)
                                #text = "we-2-0," + str(time.time()-start) + "\n"
                                #self.log_file.write(text)
                                signal.setitimer(signal.ITIMER_REAL,0)
                                return cb.vote(action_index)

                elif self.role == "POSSESSED":
                    if self.day == 1:
                        if self.talk_count == 0:
                            self.talk_count += 1
                            #text = "po-1-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.comingout(self.base_info["agentIdx"],"SEER")
                        elif self.talk_count == 1:
                            self.talk_count += 1
                            #text = "po-1-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.divined(list(self.divineIdx.keys())[0],list(self.divineIdx.values())[0])
                        elif self.talk_count == 2:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "po-1-2," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)
                    else:
                        if self.talk_count == 0:
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index,role_index = self.dqn_talk_special.get_talk(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            actions = self.onehot(action_index-1,self.playerNum)
                            roles = self.onehot(role_index-1,6)
                            self.actionLog.append(np.concatenate((actions,roles)))
                            #text = "po-2-0," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return "DIVINED AGENT[" + str(action_index) + "] " + str(decode[str(int(role_index))])

                        elif self.talk_count == 1:
                            self.talk_count += 1
                            possibleActions = self.possible()
                            state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                            state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                            state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                            state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                            state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                            state = np.concatenate(([self.day],state))
                            state = np.concatenate(([code[self.role]],state))
                            #print(self.stateLog_special)

                            action_index = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            self.stateLog.append(state)
                            #print(log_action)
                            actions = self.onehot(action_index-1,self.playerNum)
                            self.actionLog.append(actions)
                            #text = "po-2-1," + str(time.time()-start) + "\n"
                            #self.log_file.write(text)
                            signal.setitimer(signal.ITIMER_REAL,0)
                            return cb.vote(action_index)

                        else:
                            alive_num = 0
                            for i in range(self.playerNum):
                                if self.base_info["statusMap"][str(i+1)] == "ALIVE":
                                    alive_num += 1
                            if alive_num <= 3:
                                #text = "po-2-2," + str(time.time()-start) + "\n"
                                #self.log_file.write(text)
                                signal.setitimer(signal.ITIMER_REAL,0)
                                return cb.comingout(self.base_info["agentIdx"],"POSSESSED")
                            else:
                                #text = "po-2-2," + str(time.time()-start) + "\n"
                                #self.log_file.write(text)
                                signal.setitimer(signal.ITIMER_REAL,0)
                                return cb.skip()
            #text = "talk-skip," + str(time.time()-start) + "\n"
            #self.log_file.write(text)
            signal.setitimer(signal.ITIMER_REAL,0)
            return cb.skip()
        except Exception:
            print("1174timeout")
            signal.setitimer(signal.ITIMER_REAL,0)
            return cb.skip()

    def calc_reward(self):
        #if self.statusMap[str(self.index)] == "ALIVE":
        if self.myWin(self.base_info,self.diff_data):
            self.reward = 1
        else:
            self.reward = -1

    def myWin(self,base_info,diff_data):
        wolf_count, village_count = 0, 0
        for i in range(diff_data.shape[0]):
            if "WEREWOLF" in diff_data["text"][i] and base_info["statusMap"][str(i+1)] == "ALIVE":
                wolf_count+=1
            elif "POSSESSED" in diff_data["text"][i] and base_info["statusMap"][str(i+1)] == "ALIVE":
                wolf_count+=1
            elif "VILLAGER" in diff_data["text"][i] and base_info["statusMap"][str(i+1)] == "ALIVE":
                village_count+=1
            elif "SEER" in diff_data["text"][i] and base_info["statusMap"][str(i+1)] == "ALIVE":
                village_count+=1
        if ((base_info["myRole"] == "WEREWOLF" or base_info["myRole"] == "POSSESSED") and wolf_count >= village_count) or ((base_info["myRole"] == "VILLAGER" or base_info["myRole"] == "SEER") and wolf_count <= village_count):
            return True
        else:
            return False


    def finish(self):
        #self.log_file.close()
        signal.signal(signal.SIGALRM,signal_handler)
        signal.setitimer(signal.ITIMER_REAL,self.altime)
        try:
            self.dqn_vote = None
            self.dqn_talk = None
            self.dqn_special = None
            self.dqn_talk_special = None
            signal.setitimer(signal.ITIMER_REAL,0)
            return None
        except Exception:
            signal.setitimer(signal.ITIMER_REAL,0)
            return None

    def onehot(self,actionIdx,dim):
        actions = np.zeros(dim)
        #print("onehot",actions)
        actions[actionIdx-1] = 1
        #print("onehot",actions)
        return actions

    def onehot2(self,actionIdx,dim,actionRole):
        actions = np.zeros(dim)
        #print("actions",actions)
        #print("actionIdx",actionIdx)
        actions[actionIdx] = 1
        actions[self.playerNum-1+actionRole] = 1
        #print(actions)
        return actions

    def possible(self):
        possibleActions = []
        for i in range(self.playerNum):
            if self.statusMap[str(i+1)] == "ALIVE" and i+1 != self.index:
                possibleActions.append(True)
            else:
                possibleActions.append(False)

        return possibleActions

    def splitText(self, text):
        # print("splitText() start with text", text)
        temp = text.split()
        topic = temp[0]
        if topic == "ESTIMATE":
            target = int(temp[1][6:8])
            role = temp[2]
            return [topic,target,role]
        elif topic == "COMINGOUT":
            target = int(temp[1][6:8])
            role = temp[2]
            return [topic,target,role]
        elif topic == "DIVINATION":
            target = int(temp[1][6:8])
            return [topic,target]
        elif topic == "VOTE":
            target = int(temp[1][6:8])
            return [topic,target]
        elif topic == "ATTACK":
            target = int(temp[1][6:8])
            return [topic,target]
        elif topic == "DIVINED":
            target = int(temp[1][6:8])
            species = temp[2]
            return [topic,target,species]
        elif topic == "IDENTIFIED":
            target = int(temp[1][6:8])
            species = temp[2]
            return [topic,target,species]
        elif topic == "GUARDED":
            target = int(temp[1][6:8])
            return [topic,target]
        elif topic == "VOTED":
            target = int(temp[1][6:8])
            species = temp[2]
            return [topic,target]
        elif topic == "ATTACKED":
            target = int(temp[1][6:8])
            return [topic,target]
        elif topic == "AGERR":
            return [topic]
        elif topic == "DISAGREE":
            return [topic]
        else:
            return []

agent = SampleAgent(myname)


# run
if __name__ == '__main__':
    aiwolf_cp.aiwolfpy.connect_parse(agent)
