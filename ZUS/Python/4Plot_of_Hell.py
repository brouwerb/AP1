import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import roundwitherror as re
import string
muly = 1e5
mulx = 1e-6

X_START =0
Y_START =12 * muly
X_END = 4.2 * mulx
Y_END = 45.5 *muly
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"$p*V$   in   $hpa*mm^3$"
X_LABEL = r"$\frac{1}{V}$    in    $\frac{1}{cm^3}$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 1 *mulx
Y_MAJOR_TICK = 5 *muly
X_MINOR_TICK =0.2 * mulx
Y_MINOR_TICK = 1 *muly
SAVE_AS = "./ZUS/Plots/4Plot_of_Hell.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

n=0.002613
R=8.314462618
Kelvin = 273.15
def Alind(String):
    return [string.ascii_uppercase.index(String[0]),int(String[1:])-1]

def Theo(x,a,b,T):
    return n*R*T/(x-(n*b))-n**2*a/x
def TheoArr(x,p):
    return Theo(x,p[0],p[1],p[2])

def getValFromCell(Cell,path,sheet):
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    return float(worksheet.cell(Alind(Cell)[1], Alind(Cell)[0]).value)

def getAxisFromCell(Cell1,Cell2,path,sheet,plusCol=0):
    row1=Alind(Cell1)[1]
    collumn1 = Alind(Cell1)[0]+plusCol
    row2 = Alind(Cell2)[1]
    data = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    for i in range(row1,row2):
        data.append(worksheet.cell(i, collumn1).value)    
    return data

def polynom(x,a,b,c,d,e,f,g):
    return a+b*(x-g)+c*(x-g)**2+d*(x-g)**2+e*(x-g)**2+f*(x-g)**2
def polynomArr(x,p):
    return polynom(x,p[0],p[1],p[2],p[3],p[4],p[5],p[6])

TempsCell = [["B1","B53","B103"],["A1","C1","E1"],["A1","E1","I1"]]
Axis = [[[["A3","A25"],["A29","A51"]],[["A54","A76"],["A80","A101"]],[["A105","A141"],["A148","A171"]]],[[["A3","A25"],["A3","A25"]],[["C3","C25"],["C3","C25"]],[["E3","E23"],["E3","E23"]]],[[["A3","A25"],["A29","A51"]],[["E3","E25"],["E29","E51"]],[["I3","I23"],["I26","I58"]]]]
FluAb = [[[1.2,28.75],[1,34]],[[1.75,23],[1.2,30.75]],[[1.75,25],[1.3,31]]]
GaBis =[[[0.4,29],[0.4,35.75]],[[0.5,24.75],[0.5,32.5]],[[0.5,25.5],[0.6,32]]]

Temps =[]
x = []
y =[]
popt=[]
perr=[]
for i in range(3):
    Temps.append([])
    x.append([])
    y.append([])
    popt.append([])
    perr.append([])
    path = f"./ZUS/Data/G{i+1}.xls"
    for j in range(len(TempsCell[0])):
        
        Temps[i].append(getValFromCell(TempsCell[i][j],path,"Daten"))
        print (Alind(TempsCell[i][j]))
        x[i].append([getAxisFromCell(Axis[i][j][0][0],Axis[i][j][0][1],path,"Daten"),getAxisFromCell(Axis[i][j][0][0],Axis[i][j][0][1],path,"Daten")])
        y[i].append([getAxisFromCell(Axis[i][j][0][0],Axis[i][j][0][1],path,"Daten",plusCol=1),getAxisFromCell(Axis[i][j][0][0],Axis[i][j][0][1],path,"Daten",plusCol=1)])
        
        x[i][j][0]= [x[i][j][0][k]*1e-6 for k in range(len(x[i][j][0]))]
        y[i][j][0]= [y[i][j][0][k]*1e5 for k in range(len(y[i][j][0]))]
        #print(x[i][j])
        # for k,K in enumerate(x[i][j][0]):
        #     if K in x[i][j][1]:
        #         x[i][j][0][k]=K+x[i][j][1][x[i][j][1].index(K)]/2
        poptBuf,perBuf = optimize.curve_fit(Theo,x[i][j][0],y[i][j][0],bounds=[[3.95-0.01,0.000197-0.0000001,Temps[i][j]-0.01],[3.95+0.01,0.000197+0.0000001,Temps[i][j]+0.01]])
        popt[i].append(poptBuf)
        perr[i].append(np.sqrt(np.diag(perBuf)))
        print(popt[i][j])

fig, ax = plt.subplots()
ax.grid()
for i in range(len(x)):
    for j in range(len(x[i])):
        xy = re.genDataFromFunktion(200,X_START,X_END,popt[i][j],TheoArr)
        
        ax.scatter(x[i][j][0],y[i][j][0],s=10,linewidths=1,edgecolors="black",zorder=10)
        
        theo,=ax.plot(xy[0],xy[1],color= COLOR_STYLE[1],linestyle="dotted",linewidth=0.7)
ubergangs =[[],[]]
for i in range(len(FluAb)):
    for j in range(len(FluAb[0])):
        ubergangs[0].append(FluAb[i][j][0]*1e-6)
        ubergangs[0].append(GaBis[i][j][0]*1e-6)
        ubergangs[1].append(FluAb[i][j][1]*1e5)
        ubergangs[1].append(GaBis[i][j][1]*1e5)
        ax.scatter(FluAb[i][j][0]*1e-6,FluAb[i][j][1]*1e5,s=40,facecolors="none",edgecolors="purple",linewidths=1.5)
        ax.scatter(GaBis[i][j][0]*1e-6,GaBis[i][j][1]*1e5,s=40,facecolors="none",edgecolors="purple",linewidths=1.5)
polpar,polerr =optimize.curve_fit(polynom,ubergangs[0],ubergangs[1],bounds=[[-np.inf,-np.inf,-np.inf,-np.inf,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]])
pol = re.genDataFromFunktion(200,X_START,X_END,polpar,polynomArr)
ax.plot(pol[0],pol[1],color= "black",linestyle="dotted",linewidth=1)
print(polpar)

#ax.legend([sc,theo],[r"Messdaten",r"Fit : $ax+b$ mit"+"\n"+f"a={re.round_err(popt[0],perr[0])} , b={re.round_err(popt[1],perr[1])}"])
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
#ax.scatter(x,y,marker='x',color="C0")
#ax.plot([X_START,X_END],[reg.intercept,intercept+X_END*slope],color="red",linewidth=0.8)


ax.set_xlim(X_START,X_END)
ax.set_ylim(Y_START,Y_END)


# For the minor ticks, use no labels; default NullFormatter.

ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  