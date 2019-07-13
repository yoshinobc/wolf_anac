import numpy as np
import pickle as pk
import matplotlib.pyplot as plt
import time

f = open("kill_rate_log.txt",mode = "r")
loss = []
count =0
while True:
    text = f.readline()
    if not text:
        break
    ob = text.split(" ")
    count += 1
    if len(ob) == 6:
        if ob[5][1:] == "inf":
            loss.append(float("inf"))
        else:
            loss.append(float(ob[5][1:]))
    else:
        loss.append(float("inf"))
x_lists = [i for i in range(count)]
plt.plot(np.array(x_lists),np.array(loss))
plt.title("my_agent")
plt.xlabel("step")
plt.ylabel("loss_value")
plt.show()
