from matplotlib.markers import MarkerStyle
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import stats
from scipy import optimize
import math
import roundwitherror
from matplotlib.lines import Line2D

X_START =20
Y_START =3.15
X_END = 85
Y_END = 4.2
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Winkelgeschwindigkeit $\omega$ rad/s"
X_LABEL = r"Kopplungsradius $r$ in cm"
X_ERROR = 0.02
Y_ERROR = 1
X_MAJOR_TICK = 10
Y_MAJOR_TICK =0.2
X_MINOR_TICK =2
Y_MINOR_TICK = 0.05
SAVE_AS = "./SEB/plotW.pdf"
POINT_STYLE = [4,5,"x","s"]
COLOR_STYLE =["blue","red","green","purple"]

path1 = './SEB/Raw_data/1#1.txt'

indizes = [[76, 1494], [97, 1025], [81, 607], [81, 471], [102, 392], [79, 289], [72, 264], [69, 215], [50, 171], [47, 145], [58, 155], [59, 139], [60, 146], [66, 123]]


def getData(path):
    content=""
    with open (path) as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if(i!=0 and i!=len(buf)-1):
            buffer=I.split("\t")
            buffer2=[]
            for N in buffer:
                
                buffer2.append(float(N))
            content.append(buffer2)
    return content

def getPlotable(rData):
    data=[[],[]]
    for i,I in enumerate(rData):
        data[0].append(I[0])
        data[1].append(I[1])
    return data

colors = np.random.rand(2)

selectedpoints = []

for i in range(14):

    selectedpoints.append([])
    def onpick1(event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind
            
            
            
            selectedpoints[i].append(ind[0])
            selectedpoints[i].sort()
            buff = [[], []]
            for j in selectedpoints[i]:
                buff[0].append(getPlotable(getData(path1))[0][ind[0]])
                buff[1].append(getPlotable(getData(path1))[1][ind[0]])
            points = ax.scatter(buff[0], buff[1], color=COLOR_STYLE[0])
            print('onpick1 line:', np.column_stack([xdata[i], ydata[i]]), ind, buff)
            plt.draw()
    path1 = f'./POR/Raw_data/A5#{i+2}#1.txt'
    while True:
        fig, ax = plt.subplots()
        line, = ax.plot(getPlotable(getData(path1))[0], getPlotable(getData(path1))[1], picker=True, pickradius=5)
        # plt.show()
        

        fig.canvas.mpl_connect('pick_event', onpick1)
        plt.show()
        print(selectedpoints)
        if len(selectedpoints[i])==2:
            plt.close()
            break




print('end')