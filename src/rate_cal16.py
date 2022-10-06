#レート計算
import os
import pandas as pd
import numpy as np
import math
import numpy as np
from tqdm import tqdm
import time
import warnings
warnings.simplefilter("ignore")

df2 = pd.read_csv("df_merge_cl.csv", index_col=0)

df_rate = pd.DataFrame()
nr = []
df2 = df2[df2["place"]!=0]
racecode = df2["race_code"].tolist()
racecode = list(dict.fromkeys(racecode))

op = list(df2["player_id"].unique())
s_rate = [1500]*len(op)
dic = dict(zip(op,s_rate))

#初期レート定義する必要あり
for i in tqdm(racecode):

    race_rate = []
    df_cal =df2[df2["race_code"] == i]
    #ここにそのときのレートを取得する記述が必要
    uma_list = list(df_cal["player_id"])

    new_rate = [0]*len(uma_list)
    #新レート追加の引数カウント
    tc=0
    try:
        race_rate = [dic.pop(uma) for uma in uma_list]
    except KeyError:
        print(i)

    df_cal["rating"] = race_rate
    df_rate = pd.concat([df_rate, df_cal])

    #出走頭数分の箱つくる
    res_list = df_cal["place"].tolist()
    #レートを計算して血統登録番号をkeyとし格納
    count = 0
    for a,ra in zip(res_list,race_rate):
        count2 = 0
        count +=1
        Ra_s = 0
        for b,rb in zip(res_list,race_rate):
            count2 +=1
            if count == count2:
                continue
            elif a ==b:#同着
                Win = 1/(10**((rb-ra)/400)+1)
                Lose = 1-Win
                Ra_s += 16*Lose*(1/2)
                Ra_s -= 16*Win*(1/2)
            elif a < b:#a ブライアスコアを求めるならここで(Win-1)^2
                Win = 1/(10**((rb-ra)/400)+1)
                Lose = 1-Win
                Ra_s += 16*Lose

            elif a > b:#b ブライアスコアを求めるならここで(Lose-0)^2
                Win = 1/(10**((ra-rb)/400)+1)
                Lose = 1-Win
                Ra_s -= 16*Lose

        a_rate = ra + Ra_s
        umad = uma_list[count-1]
        new_dic = {umad:a_rate}
        dic.update(new_dic)

        new_rate[tc] = a_rate
        tc += 1
        #new_rate.append(a_rate)
    nr.extend(new_rate)
    new_dic = dict(zip(uma_list,new_rate))
    dic.update(new_dic)

df_rate["レース後rating"] = nr
df_rate["rate変動"] = df_rate["レース後rating"] - df_rate["rating"]

df_rate.to_csv("df_rate.csv")
