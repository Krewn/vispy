
from yahoo_finance import Share
import os

def trytryagain(k,n=3):
    try:
        tag = k[0]
        print(tag)
        stock = Share(tag)
        p = stock.get_price()
        t = stock.get_trade_datetime()
        return(k+[str(t),str(p),str((float(p)/float(k[2])-1)*100)+"%"])
    except:
        if(n>0):
            return(trytryagain(k))
        else:
            raise("YahooFinanceError","Mal-Formed Response 3x")

def PredictionStatus(fn):
    handle = open(fn,"r")
    ftext = handle.read()
    rows = [k.split("\t") for k in ftext.split("\n")]
    results = []
    for k in rows[1:]:
        try:
            results.append(trytryagain(k))
            print(results[len(results) - 1])
        except Exception as ex:
            print(ex.args)
    return(results)

def lltoCsv(opfile,ll):
    handle = open(opfile,"w")
    handle.write("\n".join(["\t".join(k) for k in ll]))
    handle.close()
    return(0)

import numpy as np
from datetime import datetime

import vis

def RollingAverage(d,w):
    ret = []
    for k in range(0,len(d)-w):
        ret.append(sum(d[k:k+w])/float(w))
    l = int(int(w)/2)
    r = int(int(w)-l)
    return([(l+n,k) for n,k in enumerate(ret)])

def plotIT(fn):
    f = open(fn,"r")
    ft = f.read()
    lines = [k.split("\t") for k in ft.split("\n")]
    y = [float(b[5][:-1]) for k,b in enumerate(lines)]
    p = [(float(b[1])-1.)*100 for k,b in enumerate(lines)]
    x = [str(b[0]) for k,b in enumerate(lines)]
    N = len(y)
    width = 0.19
    w1= int(len(y)/2)
    w2= int(len(y)/10)
    w3= int(len(y)/50)
    win1 = RollingAverage(y,w1)
    win2 = RollingAverage(y,w2)
    win3 = RollingAverage(y,w3)
    predictions = vis.drawable("Prediction",0)
    for n,k in enumerate(p):
        predictions.addData(n,k)
    performances = vis.drawable("Performance",1)
    performances.setType("bar")
    for n,k in enumerate(y):
        performances.addData(n,k)
    twoPerc = vis.drawable("2% Windows",2)
    for k in win3:
           twoPerc.addData(k[0],k[1])
    tenPerc = vis.drawable("10% Windows",3)
    for k in win2:
           tenPerc.addData(k[0],k[1])
    fiftyPerc = vis.drawable("50% Windows",4)
    for k in win1:
           fiftyPerc.addData(k[0],k[1])
    myGraph = vis.chart()
    myGraph.addDrawable(predictions)
    myGraph.addDrawable(performances)
    myGraph.addDrawable(twoPerc)
    myGraph.addDrawable(tenPerc)
    myGraph.addDrawable(fiftyPerc)
    myGraph.opGraph(fn.replace(".csv",".html"))
    

def followUpOn(fn):
    title="Appended_"+localizeFileHandle(fn[:-4])+"~"+datetime.today().strftime('%Y_%m_%d_%H_%M')+".csv"
    lltoCsv(title,PredictionStatus(fn))
    plotIT(title)

def localizeFileHandle(fh):
    return(os.path.basename(fh))

import sys

followUpOn(localizeFileHandle(sys.argv[1]))
