import json
import matplotlib.pyplot as plt

# this scipt plots the three plots: timestamp only, jaccard and tf-idf

JacEty2outs1000 = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/JacEty2outs1000.json').read())
JacWC2outs1000 = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/JacWC2outs1000.json').read())
TfidfEty2outs1000 = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/TfidfEty2outs1000.json').read())
TfidfWC2outs1000 = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/TfidfWC2outs1000.json').read())
only_time_2outs = json.loads(open(r'/Users/ZhangHaotian/desktop/LO/only_time_2outs.json').read())

lineweight = 2.5
fontsize = 20

plt.subplot(1,3,1)
x_axis = []
PCs = []
MRR1s = []
for i in only_time_2outs:
    x_axis.append(i[0])
    PCs.append(i[1][0])
    MRR1s.append(i[1][1])

plt.plot(x_axis, PCs, color="red", linewidth=lineweight, linestyle="-", label="recall@k")
plt.plot(x_axis, MRR1s, color="red", linewidth=lineweight, linestyle="--", label="MRR")
plt.legend(loc='center right' )
plt.xlabel("k", fontsize=fontsize)
plt.ylabel("accuracy metric", fontsize=fontsize)
plt.title("Timestamp Only", fontsize=fontsize)

plt.subplot(1,3,2)
x_axis = []
PCs = []
MRR1s = []
for i in JacEty2outs1000:
    x_axis.append(i[0])
    PCs.append(i[1][0])
    MRR1s.append(i[1][1])

axes = plt.gca()
axes.set_xlim([0,1000])
axes.set_ylim([0,1])

plt.plot(x_axis, PCs, color="red", linewidth=lineweight, linestyle="-", label="recall@k, entity")
plt.plot(x_axis, MRR1s, color="red", linewidth=lineweight, linestyle="--", label="MRR, entity")
plt.legend(loc='center right' )
plt.xlabel("k", fontsize=fontsize)
plt.ylabel("accuracy metric", fontsize=fontsize)
plt.title("Jaccard", fontsize=fontsize)

x_axis = []
PCs = []
MRR1s = []
for i in JacWC2outs1000:
    x_axis.append(i[0])
    PCs.append(i[1][0])
    MRR1s.append(i[1][1])

plt.plot(x_axis, PCs, color="blue", linewidth=lineweight, linestyle="-", label="recall@k, word cloud")
plt.plot(x_axis, MRR1s, color="blue", linewidth=lineweight, linestyle="--", label="MRR, word cloud")
plt.legend(loc='center right' )
plt.xlabel("k", fontsize=fontsize)
plt.ylabel("accuracy metric", fontsize=fontsize)
plt.title("Jaccard", fontsize=fontsize)

plt.subplot(1,3,3)
x_axis = []
PCs = []
MRR1s = []
for i in TfidfEty2outs1000:
    x_axis.append(i[0])
    PCs.append(i[1][0])
    MRR1s.append(i[1][1])

plt.plot(x_axis, PCs, color="red", linewidth=lineweight, linestyle="-", label="recall@k, entity")
plt.plot(x_axis, MRR1s, color="red", linewidth=lineweight, linestyle="--", label="MRR, entity")
plt.legend(loc='center right' )
plt.xlabel("k", fontsize=fontsize)
plt.ylabel("accuracy metric", fontsize=fontsize)
plt.title("TF-IDF", fontsize=fontsize)

x_axis = []
PCs = []
MRR1s = []
for i in TfidfWC2outs1000:
    x_axis.append(i[0])
    PCs.append(i[1][0])
    MRR1s.append(i[1][1])

plt.plot(x_axis, PCs, color="blue", linewidth=lineweight, linestyle="-", label="recall@k, word cloud")
plt.plot(x_axis, MRR1s, color="blue", linewidth=lineweight, linestyle="--", label="MRR, word cloud")
plt.legend(loc='center right' )
plt.xlabel("k", fontsize=fontsize)
plt.ylabel("accuracy metric", fontsize=fontsize)
plt.title("TF-IDF", fontsize=fontsize)
