#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
import pandas as pd


#=========== general settings ============================#
plt.rcParams["figure.figsize"] = [30, 10]
plt.rcParams["figure.subplot.wspace"] = 0.2

plt.rcParams["lines.linewidth"] = 5.0

plt.rcParams['font.family'] ='sans-serif'#使用するフォント
plt.rcParams['font.sans-serif'] ='Arial'#使用するフォント
plt.rcParams["font.size"] = 30
#plt.rcParams['mathtext.rm'] ='sans'#使用するフォント
#plt.rcParams['mathtext.default'] ='rm'#使用するフォント

plt.rcParams['xtick.direction'] = 'in'#x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in'#y軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['xtick.major.width'] = 1.0#x軸主目盛り線の線幅
plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
plt.rcParams["xtick.major.pad"] = 19.0
plt.rcParams["ytick.major.pad"] = 16.0
plt.rcParams["xtick.major.size"] = 10
plt.rcParams["ytick.major.size"] = 10

plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth。囲みの太さ
plt.rcParams["axes.labelpad"] = 10
#==================================================================#


dirc1 = 100
dirc2 = 110


S1 = pd.read_csv("output/5000/ST_K_G_" + str(dirc1) + ".csv", index_col=0 )
S2 = pd.read_csv("output/5000/ST_K_G_" + str(dirc2) + ".csv", index_col=0 )

ST1 = S1[["s11","s22","s33", "s12", "s13", "s23", "p0", "ts", "tv"]]
# ST1_err = S1[["s11_err","s22_err","s33_err", "s12_err", "s13_err", "s23_err", "p0_err", "ts_err", "tv_err"]]

ST2 = S2[["s11","s22","s33", "s12", "s13", "s23", "p0", "ts", "tv"]]
# ST2_err = S2[["s11_err","s22_err","s33_err", "s12_err", "s13_err", "s23_err", "p0_err", "ts_err", "tv_err"]]


fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.set_title("(a) Anelastic normal strain recovery in xx direction", loc="left", fontsize=40, pad=50)
ax2.set_title("(b) Anelastic normal strain recovery in xy direction", loc="left", fontsize=40, pad=50)



ST1.plot(ax = ax1, legend=False, style=["-", "-", "-", "-.", "-.", "-.", ":", "--", "--"])
ST2.plot(ax = ax2, style=["-", "-", "-", "-.", "-.", "-.", ":", "--", "--"])

plt.legend(loc="upper left", bbox_to_anchor=(1,1))

ax1.set_ylabel("Sensitivity")
ax1.set_xlabel("Time [hour]")
ax2.set_ylabel("Sensitivity")
ax2.set_xlabel("Time [hour]")

ax2.legend(["$\sigma_{11}$", "$\sigma_{22}$", "$\sigma_{33}$", "$\sigma_{12}$", "$\sigma_{13}$", "$\sigma_{23}$",
            "$p_{0}$", r"$\tau_{S}$", r"$\tau_{V}$"],
            loc="upper left", bbox_to_anchor=(1,1))



ax1.set_xlim([0,50])
ax2.set_xlim([0,50])

ax1.set_ylim([0,1])
ax2.set_ylim([0,1])

ax1.text(ST1.index[5], ST1["s11"].iloc[5] + 0.03, "$\sigma_{11}$")
ax1.text(ST1.index[2], ST1["ts"].iloc[2] + 0.03, r"$\tau_{S}$")
ax1.text(ST1.index[7], ST1["p0"].iloc[7] + 0.03, r"$p_{0}$")

ax2.text(ST2.index[8], ST2["s12"].iloc[8] + 0.04, "$\sigma_{12}$")
ax2.text(ST2.index[2], ST2["ts"].iloc[2] + 0.03, r"$\tau_{S}$")

fig.savefig("output/5000/ST.png", bbox_inches="tight", pad_inches=0.005)
plt.close(fig)

