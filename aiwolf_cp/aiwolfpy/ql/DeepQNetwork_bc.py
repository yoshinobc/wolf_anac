# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import os
import pickle
import collections
import random
from pathlib import Path
import glob

MAXSIZE = 1000000
INITIAL_REPLAY = 500
GAMMA = 0.99
EXPLORE = 180000.
BATCH_SIZE = 128
UPDATE_STEP = 20
FINALE_EPSILON = 0.2
EPSILON = 0.9
class DeepQNetwork_bc:
    def __init__(self,network_type_role,network_type_act,size,learning_rate = 0.001,state_size = 101,hidden1_size = 128,hidden2_size = 64,hidden3_size = 64,hidden4_size = 32):
        if size == 15:
            self.actions = size
            self.input_size = 947
            self.role = network_type_role
            self.act = network_type_act
            self.epsilon = EPSILON
            print(os.path.dirname(__file__))

            if self.act == "talk_special":
                self.actions = 21
            self.x = tf.placeholder(tf.float32, [None, self.input_size])
            fc1 = tf.reshape(self.x,[-1,self.input_size])
            fc1 = tf.contrib.layers.fully_connected(inputs=fc1, num_outputs=256, activation_fn=tf.nn.relu)
            # fc1 = tf.nn.dropout(fc1, self.dropout)
            fc2 = tf.contrib.layers.fully_connected(inputs=fc1, num_outputs=128, activation_fn=tf.nn.relu)
            # fc2 = tf.nn.dropout(fc2, self.dropout)

            fc3 = tf.contrib.layers.fully_connected(inputs=fc2,num_outputs=64,activation_fn=tf.nn.relu)
            #932,128,64,32,15のDNN
            self.QValue = tf.contrib.layers.fully_connected(inputs=fc3, num_outputs=self.actions, activation_fn=None)
            self.actionInput = tf.placeholder(tf.float32, [None, self.actions])
            self.yInput = tf.placeholder(tf.float32, [None])
            #qnnにself.actionInputとの積を入れ，その総和
            QOfAction = tf.reduce_sum(tf.multiply(self.QValue, self.actionInput), reduction_indices = 1)
            #総和と実際の行動との誤差の平均
            self.cost = tf.reduce_mean(tf.square(self.yInput - QOfAction))
            #lossはslef.QnnにactionInput()
            self.trainStep = tf.train.AdamOptimizer(1e-3).minimize(self.cost)
            self.saver = tf.train.Saver(max_to_keep=1)
            config = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1, \
                        allow_soft_placement=True, device_count = {'CPU': 1})
            self.session = tf.Session(config=config)
            self.session.run(tf.global_variables_initializer())
            print("getcwd",glob.glob(os.getcwd()+"/*"))
            print("getcwd/home/test/",glob.glob(os.getcwd()+"/home/aiwolf/contest/test/*"))
            print("getcwd/home/test/data",glob.glob(os.getcwd()+"/home/aiwolf/contest/test/data/*"))
            print("getcwd/aiwolfpy/ql",glob.glob(os.getcwd()+"/home/aiwolf/contest/test/aiwolf_cp/aiwolfpy/ql/*"))

            checkpoint = tf.train.latest_checkpoint(os.getcwd()+"/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_15/")
            if checkpoint:
                pass
            else:
                print("not1")
                checkpoint = tf.train.latest_checkpoint(os.getcwd()+"/home/aiwolf/contest/test/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_15/")
            if checkpoint:
                pass
            else:
                print("not2")
                checkpoint = tf.train.latest_checkpoint(os.getcwd()+"/home/aiwolf/contest/test/data/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_15/")
            if checkpoint:
                pass
            else:
                print("not3")
                checkpoint = tf.train.latest_checkpoint("aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_15/")
            if checkpoint:
                pass
            else:
                print("not4")
                checkpoint = tf.train.latest_checkpoint("saved_networks_" + self.role + "_" + self.act + "_15/")
            if checkpoint:
                pass
            else:
                print("not5")
                checkpoint = tf.train.latest_checkpoint("/home/aiwolf/contest/test/data/22/bc/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_15/")
            if checkpoint:
                pass
            else:
                print("not6")
                checkpoint = tf.train.latest_checkpoint(os.path.dirname(__file__)+"/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_15/")
            if checkpoint:
                pass
            else:
                print("not7")
                checkpoint = tf.train.latest_checkpoint(os.path.dirname(__file__)+"/saved_networks_" + self.role + "_" + self.act + "_15/")

            if checkpoint:
                self.saver.restore(self.session, checkpoint)
                print(self.role + "_" + self.act + "_Model was loaded successfully: ", checkpoint)
            else:
                print(self.role + "_" + self.act + "_Network weights could not be found!")
                # print("createQNetwork() end")
        else:
            self.actions = size
            self.input_size = 117
            self.role = network_type_role
            self.act = network_type_act
            self.epsilon = EPSILON


            if self.act == "talk_special":
                self.actions = 4
            self.x = tf.placeholder(tf.float32, [None, self.input_size])
            fc1 = tf.reshape(self.x,[-1,self.input_size])
            fc1 = tf.contrib.layers.fully_connected(inputs=fc1, num_outputs=64, activation_fn=tf.nn.relu)
                # fc1 = tf.nn.dropout(fc1, self.dropout)

            #fc2 = tf.contrib.layers.fully_connected(inputs=fc1, num_outputs=128, activation_fn=tf.nn.relu)
            # fc2 = tf.nn.dropout(fc2, self.dropout)
            fc2 = tf.contrib.layers.fully_connected(inputs=fc1,num_outputs=32,activation_fn=tf.nn.relu)
            #932,128,64,32,15のDNN
            self.QValue = tf.contrib.layers.fully_connected(inputs=fc2, num_outputs=self.actions, activation_fn=None)

            self.actionInput = tf.placeholder(tf.float32, [None, self.actions])
            self.yInput = tf.placeholder(tf.float32, [None])
            #qnnにself.actionInputとの積を入れ，その総和
            QOfAction = tf.reduce_sum(tf.multiply(self.QValue, self.actionInput), reduction_indices = 1)
            #総和と実際の行動との誤差の平均
            self.cost = tf.reduce_mean(tf.square(self.yInput - QOfAction))
            #lossはslef.QnnにactionInput()
            self.trainStep = tf.train.AdamOptimizer(1e-3).minimize(self.cost)
            #arg_scope = resnet_v1.resnet_arg_scope()

            self.saver = tf.train.Saver(max_to_keep=1)
            config = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1, \
                        allow_soft_placement=True, device_count = {'CPU': 1})
            self.session = tf.Session(config=config)
            self.session.run(tf.global_variables_initializer())
            print("getcwd",glob.glob(os.getcwd()+"/*"))
            print("getcwd/home/test/data/",glob.glob(os.getcwd()+"/home/aiwolf/contest/test/data/*"))
            print("getcwd/home/test/aiwolfpy",glob.glob(os.getcwd()+"/home/aiwolf/contest/test/aiwolf_cp*"))
            print("getcwd/aiwolfpy/ql",glob.glob(os.getcwd()+"/home/aiwolf/contest/test/aiwolf_cp/aiwolfpy/ql/*"))
            checkpoint = tf.train.latest_checkpoint(os.getcwd()+"/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_5/")
            """
            if checkpoint:
                pass
            else:
                print("not1")
                checkpoint = tf.train.latest_checkpoint(os.getcwd()+"/home/aiwolf/contest/test/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_5/")
            if checkpoint:
                pass
            else:
                print("not2")
                checkpoint = tf.train.latest_checkpoint(os.getcwd()+"/home/aiwolf/contest/test/data/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_5/")
            if checkpoint:
                pass
            else:
                print("not3")
                checkpoint = tf.train.latest_checkpoint("aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_5/")
            if checkpoint:
                pass
            else:
                print("not4")
                checkpoint = tf.train.latest_checkpoint("saved_networks_" + self.role + "_" + self.act + "_5/")
            if checkpoint:
                pass
            else:
                print("not5")
                checkpoint = tf.train.latest_checkpoint("/home/aiwolf/contest/test/data/22/bc/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_5/")
            if checkpoint:
                pass
            else:
                print("not6")
                checkpoint = tf.train.latest_checkpoint(os.path.dirname(__file__)+"/aiwolf_cp/aiwolfpy/ql/saved_networks_" + self.role + "_" + self.act + "_5/")
            if checkpoint:
                pass
            else:
                print("not7")
                checkpoint = tf.train.latest_checkpoint(os.path.dirname(__file__)+"/saved_networks_" + self.role + "_" + self.act + "_5/")
            """
            print(checkpoint)
            if checkpoint:
                self.saver.restore(self.session, checkpoint)
                print(self.role + "_" + self.act + "_Model was loaded successfully: ", checkpoint)
            else:
                print(self.role + "_" + self.act + "_Network weights could not be found!")

    def sample(self,batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)),size=batch_size,replace=False)
        return [self.buffer[ii] for ii in idx]



    def possible(self,action,possibleActions,num):
        for i in list(reversed(range(num))):
            if not possibleActions[int(action[i]) -1]:
                action = np.delete(action,i)
        return action

    def possible2(self,action,possibleActions,possibleAction_wolf,num):
        for i in list(reversed(range(num))):
            if not possibleActions[int(action[i])-1] or not possibleAction_wolf[int(action[i])-1]:
                action = np.delete(action,i)
        return action

    def get_action(self,possibleActions,possibleAction_wolf,state,role,num,act = None):
        action = np.zeros(num)
        action_index = 0

        if True:
            retTargetQs = self.QValue.eval(session=self.session,feed_dict = {self.x:[state]})[0]
            while True:
                action_index = np.argmax(retTargetQs)
                if possibleActions[action_index]:
                    if role == "WEREWOLF":
                        if possibleAction_wolf[action_index]:
                            action[action_index]=1
                            break
                        else:
                            retTargetQs[action_index] = float("-inf")
                    else:
                        action[action_index] = 1
                        break
                else:
                    retTargetQs[action_index] = float("-inf")
        else:
            while True:
                action_index = random.randrange(num)
                if possibleActions[action_index]:
                    action[action_index] = 1
                    break

        return action_index+1

    def get_talk(self,possibleActions,possibleAction_wolf,state,role,num,act = None):
        action_index = 0
        if True:
            retTargetQs = self.QValue.eval(session=self.session,feed_dict = {self.x:[state]})[0]
            #print(retTargetQs)
            if num==15:
                actionIdx = np.array(retTargetQs[:15])
                actionRole = np.array(retTargetQs[15:])
                #print("1",np.hstack((actionIdx,actionRole)))
                #action = self.possible(actionIdx,possibleActions,num)

                #return np.hstack((actionIdx,actionRole)),actionIdx,acrionRole
            else:
                actionIdx = np.array(retTargetQs)
                #actionRole = np.array(retTargetQs[5:]).argsort()[::-1]
        else:
            actionIdx = np.random.uniform(0,1,num)
            if num == 15:
                actionRole = np.random.uniform(0,1,6)
            else:
                pass
                #actionRole = np.random.uniform(0,1,4).argsort()[::-1]
        #print(actionIdx)
        #action = self.possible(actionIdx,possibleActions,num)
        while True:
            if role == "WEREWOLF":
                action_index = np.argmax(actionIdx)
                if possibleActions[action_index] and possibleAction_wolf[acton_index]:
                    break
                else:
                    actionIdx[action_index] = float("-inf")
            else:
                action_index = np.argmax(actionIdx)
                if possibleActions[action_index]:
                    break
                else:
                    actionIdx[action_index] = float("-inf")
        if num == 15:
            role_index = np.argmax(actionRole)
            return action_index+1,role_index+1
        else:
            return action_index+1
        #return np.hstack((actionIdx,actionRole)),actionIdx,actionRole

    def finish(self):
      pass
      #print(self.step)
      #if self.step % 1000  == 0:
      #  pickle.dump(self.buffer,open("kill_rate_replayMemory","wb+"))
      #  pickle.dump(self.step,open("kill_rate_step","wb+"))
      #  pickle.dump(self.lossValue,open("kill_rate_loss","wb+"))
        #pickle.dump(self.buffer,open(self.role + "_" + self.act + "_replayMemory","wb+"))
        #pickle.dump(self.states,open(self.role + "_" + self.act + "_states","wb+"))
        #pickle.dump(self.step,open(self.role + "_" + self.act + "_step","wb+"))
        #pickle.dump(self.lossValue,open(self.role + "_" + self.act + "_loss","wb+"))
