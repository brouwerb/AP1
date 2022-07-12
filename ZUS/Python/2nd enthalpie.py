import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
from roundwitherror import round_err
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import roundwitherror as re
import string
from copy import deepcopy

X_START =0
Y_START =10
X_END = 0.1
Y_END = 50
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Verdampfungsenthalpie in $J/mol$"
X_LABEL = r"Temperatur in $^{\circ}K$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 2
Y_MAJOR_TICK =0.5
X_MINOR_TICK =0.5
Y_MINOR_TICK = 0.1
SAVE_AS = "./ZUS/Plots/test.pdf"
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
y = []
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
        
        x[i][j][0]= [round(x[i][j][0][k], 2) for k in range(len(x[i][j][0]))]
        x[i][j][1]= [round(x[i][j][1][k], 2) for k in range(len(x[i][j][1]))]
        #y[i][j][0]= [y[i][j][0][k]*1e5 for k in range(len(y[i][j][0]))]
        #print(x[i][j])
        # for k,K in enumerate(x[i][j][0]):
        #     if K in x[i][j][1]:
        #         x[i][j][0][k]=K+x[i][j][1][x[i][j][1].index(K)]/2
        poptBuf,perBuf = optimize.curve_fit(Theo,x[i][j][0],y[i][j][0],bounds=[[3.95-0.01,0.000197-0.0000001,Temps[i][j]-0.01],[3.95+0.01,0.000197+0.0000001,Temps[i][j]+0.01]])
        popt[i].append(poptBuf)
        perr[i].append(np.sqrt(np.diag(perBuf)))
        #print(popt[i][j])

#print(Temps)
#print(x)

temp2 = []
druck = []
vg = []
vf = []

g =  0.002622 #*0.14605


for i in range(3):
    #print(i)
    for j in range(2):
        #print(j)
        for k in range(1):
            ar = y[i][j][k][(x[i][j][k].index(float(FluAb[i][j][0]))):x[i][j][k].index(float(GaBis[i][j][0]))]
            #print(ar)
            temp2.append(Temps[i][j] + 273.15)
            print(temp2)
            druck.append(sum(ar)/len(ar))
            vg.append(FluAb[i][j][0]/(g*1e6))
            vf.append(GaBis[i][j][0]/(g*1e6))
            

#print(temp2, druck)

Temptheo = np.array([20, 30, 40]) + 273.15
Drucktheo = np.array([2.108, 2.66, 3.31])*10
temps = deepcopy(temp2)
#print(temp2)
#print(temps)
temp = np.array(temp2)
druck = np.array(druck)
#print(temp2)

def exp(t, a, c):
    return c * np.exp(-a / t)

def dexp(t, val):
    return val[0] * val[1] * np.exp(-val[0] / t) / t**2

temps.sort()




plt.style.use("./AKU/AP1_style.mplstyle")


reg,err= optimize.curve_fit(exp,temp, druck*1e5)
err= np.sqrt(np.diag(err))

ex = np.linspace(0, 500, 1000)
ey = exp(ex, reg[0], reg[1])/1e5

l = []

for i in range(len(temp)):
    #print(dexp(temp[i],reg))
    
    #l.append(dexp(temp[i],reg)*temp[i]*(vg[i]-vf[i]))
    A = 2120
    
    l.append(A/temp[i]*(vg[i]-vf[i])* druck[i]*1e5)
    print(A,temp[i],druck[i]*1e5,vg[i],vf[i],l[i])


print(temp2, temps)

for i in temps:
    j = temp2.index(i)
    #print(i, j, temp2[j])
    print(f"${temp2[j]} \si{{\celsius}}$ & ${round(druck[j]*0.1, 1)} \si{{\hecto\pascal}}$ & ${round(vg[j]*1e6, -1)} \si{{\milli\litre\per\mole}} $ & $ {round(vf[j]*1e6, -1)}  \si{{\milli\litre\per\mole}} $ & $ {round(l[j])} \si{{\joule\per\mole}} $ \\\\")

with open('./ZUS/verdenthalpie.txt', 'w') as f:
   for i in temps:
    j = temp2.index(i)
    #print(i, j, temp2[j])
    f.write(f"${round(temp2[j], 1)} \si{{\kelvin}}$ & ${round(druck[j]*0.1, 2)} \ \si{{\mega\pascal}}$ & ${int(round(vg[j]*1e6, -1))} \ \si{{\milli\litre\per\mole}} $ & $ {int(round(vf[j]*1e6, -1))} \ \si{{\milli\litre\per\mole}} $ & $ {round(l[j])} \ \si{{\joule\per\mole}} $ \\\\" + "\n")

fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]

sc[0]=ax.scatter(temp,l)
#sc[1]=ax.scatter(1/Temptheo,Drucktheo)
#theo,=ax.plot(1/ex,ey, linestyle="dotted")
#ax.legend([sc[0], sc[1], theo],[r'Theoriewerte', r"Messwerte",f"fit ($c \cdot e^{{\\frac{{A}}{{T}}}}$) mit \nA= {round_err(reg[0],err[0])} und c= {round_err(reg[1]/1e5,err[1]/1e5)} hPa"],loc="best")
ax.set(xlabel=X_LABEL, ylabel=Y_LABEL)
#ax.scatter(x,y,marker='x',color="C0")
#ax.plot([X_START,X_END],[reg.intercept,intercept+X_END*slope],color="red",linewidth=0.8)


# ax.set_xlim(X_START,X_END)
# ax.set_ylim(Y_START,Y_END)



# # For the minor ticks, use no labels; default NullFormatter.
# ax.xaxis.set_major_locator(MultipleLocator(X_MAJOR_TICK))
# ax.xaxis.set_minor_locator(MultipleLocator(X_MINOR_TICK))
# ax.yaxis.set_major_locator(MultipleLocator(Y_MAJOR_TICK))
# ax.yaxis.set_minor_locator(MultipleLocator(Y_MINOR_TICK))

#print(f"der Fehler des Slopes ist: {std_err}")
plt.show()
fig.savefig(SAVE_AS)

# worksheet.cell(0, 0).value  

