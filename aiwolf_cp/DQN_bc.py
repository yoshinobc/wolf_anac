# -*- coding:utf-8 -*-
#!/usr/bin/env python
from __future__ import print_function, division

# this is main script
# simple version

import aiwolfpy
import aiwolfpy.contentbuilder as cb
from collections import deque
import numpy as np
import argparse
import sys
import os
import time
import pickle
import random
myname = 'dqn_'
import aiwolfpy.ql
code = {"WEREWOLF":1,"VILLAGER":2,"SEER":3,"POSSESSED":4,"BODYGUARD":5,"MEDIUM":6,"ANY":7,"HUMAN":8,"SELF":9}
thisRole = "VILLAGER"
class SampleAgent(object):

    def __init__(self, agent_name):
        # myname
        self.winlists = np.zeros(self.playerNum)
        self.myname = agent_name
        self.wolf_vote = aiwolfpy.ql.DeepQNetwork("WEREWOLF","vote",15)
        self.wolf_special = aiwolfpy.ql.DeepQNetwork("WEREWOLF","special",15)
        self.wolf_talk = aiwolfpy.ql.DeepQNetwork("WEREWOLF","talk",15)
        self.wolf_vote2 = aiwolfpy.ql.DeepQNetwork2("WEREWOLF","vote",5)
        self.wolf_special2 = aiwolfpy.ql.DeepQNetwork2("WEREWOLF","special",5)
        self.wolf_talk2 = aiwolfpy.ql.DeepQNetwork("WEREWOLF","talk",5)


        self.vill_vote = aiwolfpy.ql.DeepQNetwork("VILLAGER","vote",15)
        self.vill_talk = aiwolfpy.ql.DeepQNetwork("VILLAGER","talk",15)
        self.vill_vote2 = aiwolfpy.ql.DeepQNetwork2("VILLAGER","vote",5)
        self.vill_talk2 = aiwolfpy.ql.DeepQNetwork2("VILLAGER","talk",5)

        self.seer_talk = aiwolfpy.ql.DeepQNetwork("SEER","talk",15)
        self.seer_vote = aiwolfpy.ql.DeepQNetwork("SEER","vote",15)
        self.seer_special = aiwolfpy.ql.DeepQNetwork("SEER","special",15)
        self.seer_talk_special = aiwolfpy.ql.DeepQNetwork("SEER","talk_special",15)
        self.seer_talk2 = aiwolfpy.ql.DeepQNetwork2("SEER","talk",5)
        self.seer_vote2 = aiwolfpy.ql.DeepQNetwork2("SEER","vote",5)
        self.seer_special2 = aiwolfpy.ql.DeepQNetwork2("SEER","special",5)
        self.seer_talk_special2 = aiwolfpy.ql.DeepQNetwork2("SEER","talk_special",5)

        self.poss_talk_special = aiwolfpy.ql.DeepQNetwork("POSSESSED","talk_special",15)
        self.poss_vote = aiwolfpy.ql.DeepQNetwork("POSSESSED","vote",15)
        self.poss_talk = aiwolfpy.ql.DeepQNetwork("POSSESSED","talk",15)
        self.poss_talk_special2 = aiwolfpy.ql.DeepQNetwork2("POSSESSED","talk_special",5)
        self.poss_vote2 = aiwolfpy.ql.DeepQNetwork2("POSSESSED","vote",5)
        self.poss_talk2 = aiwolfpy.ql.DeepQNetwork2("POSSESSED","talk",5)


        self.guard_vote = aiwolfpy.ql.DeepQNetwork("BODYGUARD","vote",15)
        self.guard_talk = aiwolfpy.ql.DeepQNetwork("BODYGUARD","talk",15)
        self.guard_special = aiwolfpy.ql.DeepQNetwork("BODYGUARD","special",15)
        self.guard_vote2 = aiwolfpy.ql.DeepQNetwork2("BODYGUARD","vote",5)
        self.guard_talk2 = aiwolfpy.ql.DeepQNetwork2("BODYGUARD","talk",5)
        self.guard_special2 = aiwolfpy.ql.DeepQNetwork2("BODYGUARD","special",5)

        self.medi_vote = aiwolfpy.ql.DeepQNetwork("MEDIUM","vote",15)
        self.medi_talk = aiwolfpy.ql.DeepQNetwork("MEDIUM","talk",15)
        self.medi_vote2 = aiwolfpy.ql.DeepQNetwork2("MEDIUM","vote",5)
        self.medi_talk2 = aiwolfpy.ql.DeepQNetwork2("MEDIUM","talk",5)


    def getName(self):
        return self.myname

    def initialize(self, base_info, diff_data, game_setting):
        #print("Initialize")
        self.playerNum = len(base_info["statusMap"])
        self.role = base_info["myRole"]

        if self.role == "VILLAGER":
            if self.playerNum == 15:
                self.dqn_vote = self.vill_vote
                self.dqn_talk = self.vill_talk
            else:
                self.dqn_vote = self.vill_vote2
                self.dqn_talk = self.vill_talk2

        elif self.role == "WEREWOLF":
            if self.playerNum == 15:
                self.dqn_vote = self.wolf_vote
                self.dqn_special = self.wolf_special
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

        elif self.role == "POSSESSED":
            if self.playerNum == 15:
                self.dqn_vote = self.poss_vote
                self.dqn_talk = self.poss_talk
                self.dqn_talk_special = self.poss_talk_special
            else:
                self.dqn_vote = self.poss_vote2
                self.dqn_talk = self.poss_talk2
                self.dqn_talk_special = self.poss_talk_special2

        elif self.role == "MEDIUM":
            if self.playerNum == 15:
                self.dqn_vote = self.medi_vote
                self.dqn_talk = self.medi_talk
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
        self.reward = 0


    def update(self, base_info, diff_data, request):
        #print(self.day,"update")
        #print(diff_data)
        self.base_info = base_info
        self.diff_data = diff_data
        self.statusMap = base_info["statusMap"]
        if len(diff_data) == 0 or not self.islearn:
            #print(self.day,"return")
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


    def attack(self):
        if self.day == 0 and self.whisper_count == 0:
            self.whisper_count += 1
            #print("307")
            self.attackIdx = np.argmax(self.winlists)+1
            return self.attackIdx
        elif self.day != 0 and self.whisper_count == 0:
            self.whisper_count += 1
            #print("312")
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
            """
            if len(self.stateLog_special) != 0 and len(self.actionLog_special) != 0:
                assert self.playerNum == len(self.actionLog_special[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog_special[-1]))
                self.dqn_special.update_DQN(self.stateLog_special[-1], state, self.actionLog_special[-1], 0, False,self.gamecount,self.playerNum)
            """
            actions,log_action = self.dqn_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
            i = 0
            while True:
                actionIdx = actions[i]
                if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                    self.stateLog_special.append(state)
                    #print(log_action)
                    actions = self.onehot(actionIdx-1,len(log_action))
                    #print(actions)
                    self.actionLog_special.append(actions)
                    self.attackIdx = actionIdx
                    return actionIdx
                else:
                    i += 1

    def divine(self):
        #print("divine")
        possibleActions = self.possible()
        state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
        state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
        state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
        state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
        state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
        state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
        state = np.concatenate(([self.day],state))
        state = np.concatenate(([code[self.role]],state))
        """
        if len(self.stateLog_special) != 0 and len(self.actionLog_special) != 0:
            assert self.playerNum == len(self.actionLog_special[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog_special[-1]))
            self.dqn_special.update_DQN(self.stateLog_special[-1], state, self.actionLog_special[-1], 0, False,self.gamecount,self.playerNum)
        """
        actions,log_action = self.dqn_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
        i = 0
        while True:
            actionIdx = actions[i]
            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                self.stateLog_special.append(state)
                actions = self.onehot(actionIdx-1,len(log_action))
                self.actionLog_special.append(actions)
                return actionIdx
            else:
                i += 1


    def vote(self):
        #print("vote")
        possibleActions = self.possible()
        state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
        state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
        state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
        state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
        state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
        state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
        state = np.concatenate(([self.day],state))
        state = np.concatenate(([code[self.role]],state))
        """
        if len(self.stateLog_vote) != 0 and len(self.actionLog_vote) != 0:
            assert self.playerNum == len(self.actionLog_vote[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog_vote[-1]))
            self.dqn_vote.update_DQN(self.stateLog_vote[-1], state, self.actionLog_vote[-1], 0, False,self.gamecount,self.playerNum)
        """
        actions,log_action = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
        i = 0
        while True:
            actionIdx = actions[i]
            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                self.stateLog_vote.append(state)
                actions = self.onehot(actionIdx-1,len(log_action))
                self.actionLog_vote.append(actions)
                self.voteIdx = actionIdx
                return actionIdx
            else:
                i += 1
    def guard(self):
        #print("guard")
        possibleActions = self.possible()
        state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
        state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
        state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
        state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
        state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
        state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
        state = np.concatenate(([self.day],state))
        state = np.concatenate(([code[self.role]],state))
        """
        if len(self.stateLog_special) != 0 and len(self.actionLog_special) != 0:
            assert self.playerNum == len(self.actionLog_special[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog_special[-1]))
            self.dqn_special.update_DQN(self.stateLog_special[-1], state, self.actionLog_special[-1], 0, False,self.gamecount,self.playerNum)
        """
        actions,log_action = self.dqn_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
        i = 0
        while True:
            actionIdx = actions[i]
            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                self.stateLog_special.append(state)
                #print(log_action)
                actions = self.onehot(actionIdx-1,len(log_action))
                #print(actions)
                self.actionLog_special.append(actions)
                return actionIdx
            else:
                i += 1

    def dayStart(self):
        #print("dayStart")
        #print("dayStart")
        self.talk_count = 0
        self.whisper_count = 0
        self.action_flag = False
        self.action = None
        self.voteaction = None
        self.day += 1
        self.wolfvotezeroday = {}
        return None

    def talk(self):
        if self.playerNum == 5:
            if self.role == "VILLAGER" :
                if self.talk_count == 0:
                    self.talk_count += 1
                    return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
                elif self.talk_count == 1:
                    self.talk_count += 1
                    if self.day == 1:
                        return cb.vote(np.argmax(self.winlists)+1)
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
                        """
                        if len(self.stateLog) != 0 and len(self.actionLog) != 0:
                            assert self.playerNum == len(self.actionLog[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog[-1]))
                            self.dqn_talk.update_DQN(self.stateLog[-1], state, self.actionLog[-1], 0, False,self.gamecount,self.playerNum)
                        """
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)
                            else:
                                i += 1
                elif self.talk_count == 2 and self.day == 1:
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
                    actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                    i = 0
                    while True:
                        actionIdx = actions[i]
                        if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                            self.stateLog.append(state)
                            actions = self.onehot(actionIdx-1,len(log_action))
                            self.actionLog.append(actions)
                            return cb.vote(actionIdx)
                        else:
                            i += 1

            elif self.role == "WEREWOLF":
                if self.talk_count == 0:
                    self.talk_count += 1
                    return cb.comingout(self.base_info["agentIdx"],"VILLAGER")
                elif self.talk_count == 1:
                    self.talk_count += 1
                    if self.day == 1:
                        return  cb.vote(np.argmax(self.winlists)+1)
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
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)
                            else:
                                i += 1
                elif self.talk_count == 2 and self.day == 1:
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
                    actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                    i = 0
                    while True:
                        actionIdx = actions[i]
                        if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                            self.stateLog.append(state)
                            actions = self.onehot(actionIdx-1,len(log_action))
                            self.actionLog.append(actions)
                            return cb.vote(actionIdx)
                        else:
                            i += 1

            elif self.role == "SEER":
                if self.talk_count == 0:
                    self.talk_count += 1
                    return cb.comingout(self.base_info["agentIdx"],"SEER")
                elif self.talk_count == 1:
                    self.talk_count += 1
                    if self.day == 1:
                        return cb.vote(np.argmax(self.winlists)+1)
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
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)
                            else:
                                i += 1
                elif self.talk_count == 2:
                    possibleActions = self.possible()
                    state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                    state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                    state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                    state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                    state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                    state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                    state = np.concatenate(([self.day],state))
                    state = np.concatenate(([code[self.role]],state))
                    """
                    if len(self.stateLog_talk) != 0 and len(self.actionLog_talk) != 0:
                        assert self.playerNum == len(self.actionLog_talk[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog_talk[-1]))
                        self.dqn_talk_special.update_DQN(self.stateLog_talk[-1], state, self.actionLog_talk[-1], 0, False,self.gamecount,self.playerNum)
                    """
                    actions,log_action = self.dqn_talk_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum,"talk_special")
                    i = 0
                    while True:
                        actionIdx = actions[i]
                        if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                            self.stateLog_talk.append(state)
                            actions = self.onehot(actionIdx-1,len(log_action))
                            self.actionLog_talk.append(actions)
                            return cb.comingout(actionIdx,"WEREWOLF")
                        else:
                            i += 1
                        if i == self.playerNum:
                            return cb.skip()

        elif self.role == "POSSESSED":
            if self.talk_count == 0:
                self.talk_count += 1
                return cb.comingout(self.base_info["agentIdx"],"SEER")
            elif self.talk_count == 1:
                self.talk_count += 1
                if self.day == 1:
                    return cb.vote(np.argmax(self.winlists)+1)
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
                    actions,log_action = self.dqn_talk_special.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum,"talk_special")
                    i = 0
                    while True:
                        actionIdx = actions[i]
                        if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                            self.stateLog_talk.append(state)
                            actions = self.onehot(actionIdx-1,len(log_action))
                            self.actionLog_talk.append(actions)
                            return cb.comingout(actionIdx,"WEREWOLF")
                        else:
                            i += 1
                        if i == self.playerNum:
                            return cb.skip()

            elif self.talk_count == 2:
                possibleActions = self.possible()
                state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                state = np.concatenate(([self.day],state))
                state = np.concatenate(([code[self.role]],state))
                actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                i = 0
                while True:
                    actionIdx = actions[i]
                    if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                        self.stateLog.append(state)
                        actions = self.onehot(actionIdx-1,len(log_action))
                        self.actionLog.append(actions)
                        return cb.vote(actionIdx)

        else:
            if self.role == "VILLAGER":
                if self.day == 1:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        return cb.vote(np.argmax(self.winlists)+1)
                    elif self.talk_count == 1:
                        possibleActions = self.possible()
                        state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                        state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                        state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                        state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                        state = np.concatenate(([self.day],state))
                        state = np.concatenate(([code[self.role]],state))
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)
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
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)
                    else:
                        self.talk_count += 1
                        return cb.skip()

            elif self.role == "SEER":
                if self.day == 1:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        return cb.comingout(self.base_info["agentIdx"],"SEER")
                    elif self.talk_count == 1:
                        self.talk_count += 1
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
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)
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
                        log_action,actions,actionRole = self.dqn_talk_special.get_talk(possibleActions,self.possiblewolf,state,self.role,self.playerNum,"talk_special")
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog_talk.append(state)
                                actions = self.onehot2(actionIdx,len(log_action),int(actionRole[0]))
                                self.actionLog_talk.append(actions)
                                return "DIVINED AGENT[" + str(actionIdx) + "] " + str(decode[str(int(actionRole[0])+1)])
                            else:
                                i += 1
                            if i == self.playerNum:
                                return cb.skip()

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
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)

            elif self.role == "MEDIUM":
                if self.day == 1:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        return cb.comingout(self.base_info["agentIdx"],"MEDIUM")
                else:
                    if self.talk_count == 0:
                        self.talk_count += 1
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
                        actions,log_action = self.dqn_talk.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog.append(actions)
                                return cb.vote(actionIdx)
            elif self.role == "BODYGUARD":
                if self.day == 1:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        return cb.vote(np.argmax(self.winlists)-1)
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
                        actions,log_action = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog_vote.append(state)
                                #print(log_action)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                #print(actions)
                                self.actionLog_vote.append(actions)
                                self.voteIdx = actionIdx
                                return cb.vote(actionIdx)
                            else:
                                i += 1
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
                        actions,log_action = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog_vote.append(state)
                                #print(log_action)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                #print(actions)
                                self.actionLog_vote.append(actions)
                                self.voteIdx = actionIdx
                                return cb.vote(actionIdx)
                            else:
                                i += 1
                    else:
                        self.talk_count += 1
                        return cb.skip()

            elif self.role == "WEREWOLF":
                if self.day == 1:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        return cb.vote(np.argmax(self.winlists[0])-1)
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
                        actions,log_action = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog_vote.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog_vote.append(actions)
                                self.voteIdx = actionIdx
                                return cb.vote(actionIdx)
                            else:
                                i += 1
                            if i == self.playerNum:
                                return cb.skip()
                else:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        self.talk_count += 1
                        if len(list(self.wolfvotezeroday.values())) >= 1:
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
                            actions,log_action = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                            i = 0
                            while True:
                                actionIdx = actions[i]
                                if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                    self.stateLog_vote.append(state)
                                    actions = self.onehot(actionIdx-1,len(log_action))
                                    self.actionLog_vote.append(actions)
                                    self.voteIdx = actionIdx
                                    return cb.vote(actionIdx)
                                else:
                                    i += 1
                    else:
                        self.talk_count += 1
                        return cb.skip()
            elif self.role == "POSSESSED":
                if self.day == 1:
                    if self.talk_count == 0:
                        self.talk_count += 1
                        return cb.comingout(self.base_info["agentIdx"],"SEER")
                    elif self.talk_count == 1:
                        possibleActions = self.possible()
                        state = np.concatenate((self.stateEs.reshape([self.playerNum*self.playerNum]),self.stateCo.reshape([self.playerNum*self.playerNum])))
                        state = np.concatenate((self.stateVote.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalk.reshape([self.playerNum*self.playerNum]),state))
                        state = np.concatenate((self.stateTalkNum.reshape([self.playerNum]),state))
                        state = np.concatenate((self.stateIsAlive.reshape([self.playerNum]),state))
                        state = np.concatenate((self.dayvote.reshape([self.playerNum]),state))
                        state = np.concatenate(([self.day],state))
                        state = np.concatenate(([code[self.role]],state))
                        actions,log_action = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog_vote.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog_vote.append(actions)
                                self.voteIdx = actionIdx
                                return cb.vote(actionIdx)
                            else:
                                i += 1
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
                        actions,log_action = self.dqn_vote.get_action(possibleActions,self.possiblewolf,state,self.role,self.playerNum)
                        i = 0
                        while True:
                            actionIdx = actions[i]
                            if actionIdx != self.base_info["agentIdx"] and self.statusMap[str(actionIdx)] == "ALIVE":
                                self.stateLog_vote.append(state)
                                actions = self.onehot(actionIdx-1,len(log_action))
                                self.actionLog_vote.append(actions)
                                self.voteIdx = actionIdx
                                return cb.vote(actionIdx)
                            else:
                                i += 1
                    else:
                        alive_num = 0
                        for i in range(self.playerNum):
                            if self.base_info["statusMap"][str(i+1)] == "ALIVE":
                                alive_num += 1
                        if alive_num <= 3:
                            return cb.comingout(self.base_info["agentIdx"],"POSSESSED")
                        else:
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
        if self.islearn and self.finishCount == 0:
            self.calc_reward()
            #print(self.reward)
            #print("finish")
            if self.playerNum == 15:
                if self.reward == 1:
                    state = np.ones([945]) * 10
                else:
                    state = np.ones([945]) * (-10)
                state = np.concatenate(([code[self.role],self.day],state.reshape([945])))
            else:
                if self.reward == 1:
                    state = np.ones([115]) * 10
                else:
                    state = np.ones([115]) * (-10)
                state = np.concatenate(([code[self.role],self.day],state.reshape([115])))
            """
            if len(self.stateLog_vote) != 0 and len(self.actionLog_vote) != 0:
                assert self.playerNum == len(self.actionLog_vote[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog_vote[-1]))
                self.dqn_vote.update_DQN(self.stateLog_vote[-1],state,self.actionLog_vote[-1],self.reward,True,self.gamecount,self.playerNum)
            if len(self.stateLog) != 0 and len(self.actionLog) != 0:
                self.dqn_talk.update_DQN(self.stateLog[-1],state,self.actionLog[-1],self.reward,True,self.gamecount,self.playerNum)
            if self.role == "VILLAGER" or self.role == "POSSESSED":
                pass
            else:
                if len(self.stateLog_special) != 0 and len(self.actionLog_special) != 0:
                    assert self.playerNum == len(self.actionLog_special[-1]), '期待[{0}], 入力[{1}]'.format(str(self.playerNum), len(self.actionLog_special[-1]))
                    self.dqn_special.update_DQN(self.stateLog_special[-1],state,self.actionLog_special[-1],self.reward,True,self.gamecount,self.playerNum)
            """
            #pickle.dump(self.gamecount,open("kill_rate_gamecount","wb+"))
            self.finishCount += 1
            """
            self.dqn_talk.finish()
            self.dqn_vote.finish()
            if self.role == "WEREWOLF" or self.role == "SEER" or self.role == "BODYGUARD" or self.role == "MEDIUM":
                self.dqn_special.finish()
            if self.role == "POSSESSED" and self.role == "SEER":
                self.dqn_talk_special.finish()
            """
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
    aiwolfpy.connect_parse(agent)
