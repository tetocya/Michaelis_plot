#モジュールのimport scipyとseabornは入ってないかも
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import seaborn as sns


#初濃度のリスト
x = [0.015,0.02,0.03,0.05,0.1,0.2,
     0.015,0.02,0.03,0.05,0.1,0.2]
#初速度のリスト
y = [0.361174847,0.435143456,0.451901969,0.527026337,0.601572825,0.666873238,
     0.357129689,0.443233772,0.42589738,0.558231844,0.642024408,0.674963554]
data_1 = pd.DataFrame({'Initial concentration of substrate[S](M)': x, 'Initial speed[V0](µmol/min)': y,})
#print(data_1)
#sns.scatterplot(data = data_1, x = "Initial concentration of substrate[S](M)", y = "Initial speed[V0](µmol/min)")
#ミカエリスメンテン式
#k1がVmax, k2がKm
def MM_Eq(x,k1,k2): 
    return  k1*x/(x+k2)
param, cov = curve_fit(MM_Eq,data_1["Initial concentration of substrate[S](M)"],data_1["Initial speed[V0](µmol/min)"])
print(param)
print(cov)
#曲線に使用する点の数
RES = 100

#maxは濃度の最大値
def graph_plot(max, k1, k2): 
  limit = max + max/10
  x = []
  y = []
  lst = range(0,RES + 1)
  for j in lst:
    i = max/RES * j
    x.append(i)
    y.append(MM_Eq(i,k1,k2))
  return x, y
xs, ys = graph_plot(data_1["Initial concentration of substrate[S](M)"].max(),param[0],param[1])
curve = pd.DataFrame({'Initial concentration of substrate[S](M)': xs, 'Initial speed[V0](µmol/min)': ys,})
print(curve)
#sns.scatterplot(data = curve, x = "Initial concentration of substrate[S](M)", y = "Initial speed[V0](µmol/min)", )
#入力データの描画
plt.scatter(data = data_1, x = "Initial concentration of substrate[S](M)", y = "Initial speed[V0](µmol/min)")
#fittingした関数の描画
sns.lineplot(data = curve, x = "Initial concentration of substrate[S](M)", y = "Initial speed[V0](µmol/min)", legend=False)
#Vmaxの表示
Vmax = data_1["Initial speed[V0](µmol/min)"].max()*1.1
plt.hlines(y=Vmax, xmin=0, xmax=0.200)

plt.text(0.1, 0.3, "Vmax={:.3g}µmol/min".format(Vmax))
plt.text(0.1, 0.25, "1/2Vmax={:.3g}µmol/min".format(Vmax/2))
#Kmの計算
Km_num = Vmax/2
#1/2Vmaxに最も近い初速度V0を求める(curveリスト内のindexが返ってくる)
index = curve.index[(curve["Initial speed[V0](µmol/min)"]-Km_num).abs().argsort()][0].tolist()
#求めた点の初濃度を求める
Km = curve["Initial concentration of substrate[S](M)"][index]
print(index)
print(Km)
plt.text(0.1, 0.20, "Km={:.3g}M".format(Km))
#Kmと1/2Vmaxの赤線
plt.hlines(y=Vmax/2, xmin=0, xmax=Km, color="r")
plt.vlines(x=Km, ymin=0, ymax=Vmax/2, color="r")

plt.text(0.022, 0.75, "Vmax")
plt.text(-0.01, 0.4, "1/2Vmax")
plt.text(0.022, 0.3, "Km")
#pngでファイル保存, ホームディレクトリに出力されます
plt.savefig('Michaelis_day4.png')
