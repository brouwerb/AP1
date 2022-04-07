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

indizes = [[[10, 44], [18, 54], [16, 47]], [[12, 36], [16, 41], [19, 36]], [[5, 23], [6, 24], [6, 24]], [[5, 29], [10, 30], 
[5, 25]]]


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
def onpick1(event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind
            if ind in selectedpoints:
                selectedpoints.remove(ind)
            else:
                selectedpoints.append(ind)
            selectedpoints.sort()
            buff = [[], []]
            for i in selectedpoints:
                buff[0].append(getPlotable(getData(path1))[0][ind[0]])
                buff[1].append(getPlotable(getData(path1))[1][ind[0]])
            points = ax.scatter(buff[0], buff[1], color=COLOR_STYLE[0])
            print('onpick1 line:', np.column_stack([xdata[ind], ydata[ind]]), ind, buff)
            plt.draw()
for angle in range(4):
    selectedpoints.append([])
    for durch in range(3):
        selectedpoints[angle].append([])
        def onpick1(event):
            if isinstance(event.artist, Line2D):
                thisline = event.artist
                xdata = thisline.get_xdata()
                ydata = thisline.get_ydata()
                ind = event.ind
                
                if ind[0] in selectedpoints[angle][durch]:
                    selectedpoints[angle][durch].remove(ind) # 
                else:
                    selectedpoints[angle][durch].append(ind[0])
                selectedpoints[angle][durch].sort()
                buff = [[], []]
                for i in selectedpoints[angle][durch]:
                    buff[0].append(getPlotable(getData(path1))[0][ind[0]])
                    buff[1].append(getPlotable(getData(path1))[1][ind[0]])
                points = ax.scatter(buff[0], buff[1], color=COLOR_STYLE[0])
                print('onpick1 line:', np.column_stack([xdata[ind], ydata[ind]]), ind, buff)
                plt.draw()
        path1 = f'./SEB/Raw_data/{angle+1}#{durch+1}.txt'
        while True:
            fig, ax = plt.subplots()
            line, = ax.plot(getPlotable(getData(path1))[0], getPlotable(getData(path1))[1], picker=True, pickradius=5)
            # plt.show()
            

            fig.canvas.mpl_connect('pick_event', onpick1)
            plt.show()
            print(selectedpoints)
            if len(selectedpoints[angle][durch])==2:
                plt.close()
                break

# 3, for example, is tolerance for picker i.e, how far a mouse click from
# the plotted point can be registered to select nearby data point/points.

def on_pick(event):
    global points
    line = event.artist
    xdata, ydata = line.get_data()
    print('selected point is:',np.array([xdata[ind], ydata[ind]]).T)

# cid = fig.canvas.mpl_connect('pick_event', on_pick)


def pick_simple():
    # simple picking, lines, rectangles and text
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_title('click on points, rectangles or text', picker=True)
    ax1.set_ylabel('ylabel', picker=True, bbox=dict(facecolor='red'))
    line, = ax1.plot(rand(100), 'o', picker=True, pickradius=5)

    # pick the rectangle
    ax2.bar(range(10), rand(10), picker=True)
    for label in ax2.get_xticklabels():  # make the xtick labels pickable
        label.set_picker(True)

    def onpick1(event):
        if isinstance(event.artist, Line2D):
            thisline = event.artist
            xdata = thisline.get_xdata()
            ydata = thisline.get_ydata()
            ind = event.ind
            print('onpick1 line:', np.column_stack([xdata[ind], ydata[ind]]))
        elif isinstance(event.artist, Rectangle):
            patch = event.artist
            print('onpick1 patch:', patch.get_path())
        elif isinstance(event.artist, Text):
            text = event.artist
            print('onpick1 text:', text.get_text())

    fig.canvas.mpl_connect('pick_event', onpick1)




print('end')