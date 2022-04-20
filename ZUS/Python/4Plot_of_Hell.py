import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import roundwitherror as re
import string

n=0.002613
R=8.314462618
Kelvin = 273.15
muly = 1*0.1#1e5
mulx = 1*1/n#1e-6
Tempgenau =0.1
fehlerDruck = 0.05

X_START =0
Y_START =12 * muly
X_END = 4.2 * mulx
Y_END = 45.5 *muly
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Druck $p$ in $mpa$"
X_LABEL = r"Molares Volumen $V_m$ in $\frac{cm^3}{mol}$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 250
Y_MAJOR_TICK = 5 *muly
X_MINOR_TICK = 50
Y_MINOR_TICK = 1 *muly
SAVE_AS = "./ZUS/Plots/4Plot_of_Hell.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]



def Alind(String):
    return [string.ascii_uppercase.index(String[0]),int(String[1:])-1]

def Theo(x,a,b,c,d,e,g):
    return a+b*(x-g)+c*(x-g)**2+d*(x-g)**3+e*(x-g)**4


def TheoArr(x,p):
    return Theo(x,p[0],p[1],p[2],p[3],p[4],p[5])

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

def polynom(x,a,b,c,d,e,g):
    return a+b*(x-g)+c*(x-g)**2+d*(x-g)**3+e*(x-g)**4
def polynomArr(x,p):
    return polynom(x,p[0],p[1],p[2],p[3],p[4],p[5])
def exp(x,a,b,d):
    return a+np.exp(-b*(x-d))
def expArr(x,p):
    return exp(x,p[0],p[1],p[2])
def fehlerVM(V):
    un = 1.6e-5
    uV = 0.05
    return np.sqrt((1/n*uV)**2+(V/n**2*un)**2)



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
        
        x[i][j][0]= [x[i][j][0][k]*mulx for k in range(len(x[i][j][0]))]
        y[i][j][0]= [y[i][j][0][k]*muly for k in range(len(y[i][j][0]))]
        #print(x[i][j])
        # for k,K in enumerate(x[i][j][0]):
        #     if K in x[i][j][1]:
        #         x[i][j][0][k]=K+x[i][j][1][x[i][j][1].index(K)]/2
        #poptBuf,perBuf = optimize.curve_fit(Theo,x[i][j][0],y[i][j][0],bounds=[[-np.inf,-np.inf,-np.inf,-np.inf,-np.inf,-np.inf],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]])
        #popt[i].append(poptBuf)
        #perr[i].append(np.sqrt(np.diag(perBuf)))
        #print(popt[i][j])

fig, ax = plt.subplots()
ax.grid()
for i in range(len(x)):
    for j in range(len(x[i])):
        #xy = re.genDataFromFunktion(200,X_START,X_END,popt[i][j],TheoArr)
        if i ==2 and j==2:
            ax.errorbar(x[i][j][0],y[i][j][0],fmt="none",yerr=fehlerDruck,xerr=[fehlerVM(x[i][j][0][k]/mulx) for k in range(len(x[i][j][0]))],ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8,
            color=COLOR_STYLE[0],zorder=11)
        
        ax.scatter(x[i][j][0],y[i][j][0],s=10,linewidths=0.5,edgecolors="black",zorder=10)
        
        #theo,=ax.plot(xy[0],xy[1],color= COLOR_STYLE[1],linestyle="dotted",linewidth=0.7)
ubergangs =[[],[]]
for i in range(len(FluAb)):
    for j in range(len(FluAb[0])):
        ubergangs[0].append(FluAb[i][j][0]*mulx)
        ubergangs[0].append(GaBis[i][j][0]*mulx)
        ubergangs[1].append(FluAb[i][j][1]*muly*10)
        ubergangs[1].append(GaBis[i][j][1]*muly*10)
        ax.scatter(FluAb[i][j][0]*mulx,FluAb[i][j][1]*muly,s=40,facecolors="none",edgecolors="orange",linewidths=1.5)
        ax.scatter(GaBis[i][j][0]*mulx,GaBis[i][j][1]*muly,s=40,facecolors="none",edgecolors="purple",linewidths=1.5)
polpar,polerr =optimize.curve_fit(polynom,ubergangs[0],ubergangs[1],bounds=[[34,2e-2,-5e-4,0,-9e-10,150],[40,5e-2,-2e-4,7e-6,0,200]])
pol = re.genDataFromFunktion(200,X_START,X_END,polpar,polynomArr)

ax.plot(pol[0],[pol[1][i]*0.1 for i in range(len(pol[1]))],color= "black",linestyle="--",linewidth=1)

buf =0
for i in range(len(pol[1])):
    if pol[1][i]*0.1>=buf:
        buf = pol[1][i]*0.1
upper=[[],[buf,buf]]    
upper[0].append(pol[0][pol[1].index(buf*10)])
upper[0].append(pol[0][pol[1].index(buf*10)]+1)
upper[0].append(166)
upper[1].append(4)
print(upper)
pUpper,jkh= optimize.curve_fit(exp,upper[0],upper[1],bounds=[[2,0.06,150],[5,0.065,200]])
print(pUpper)
upperPlot = re.genDataFromFunktion(200,X_START,pol[0][pol[1].index(buf*10)],pUpper,expArr)
ax.plot(upperPlot[0],upperPlot[1],color= "black",linestyle="--",linewidth=1)


#ax.fill_between([X_START,X_END],[Y_START,Y_START],[Y_END,Y_END],color ="green",alpha=0.5)
ax.fill_between(pol[0],[pol[1][i]*0.1 for i in range(len(pol[1]))],[0 for i in range(len(pol[0]))],color ="yellow",alpha=0.2)

a= pol[0][pol[1].index(buf*10):].copy()

a = upperPlot[0]+a
a.append(X_END)
b = pol[1][pol[1].index(buf*10):].copy()
b= [b[i]*0.1 for i in range(len(b))]
b.append(Y_START)
b = upperPlot[1] + b
c = [Y_END for i in range(len(b))]
ax.fill_between(a,b,c,color ="pink",alpha=0.4)

a = pol[0][:pol[1].index(buf*10)].copy()
a = [X_START]+ a
b = pol[1][:pol[1].index(buf*10)].copy()
b= [b[i]*0.1 for i in range(len(b))]
b = [Y_START]+ b
c = [expArr(a[i],pUpper)  if expArr(a[i],pUpper)<Y_END else Y_END for i in range(len(a))]
print(b)
print(c)
ax.fill_between(a,b,c,color ="green",alpha=0.2)
Temps =[re.round_err(Temps[i][j],Tempgenau) + r" $°$"for i in range(len(Temps)) for j in range(len(Temps[i]))]
Temps.append("Kondensationspunkt")
Temps.append("Vollständig flüssig")

ax.text(200, 1.7, "Koexistenzbereich")
ax.text(550, 3.7, "nur Gas")
ax.text(45,3,"nur flüssig",rotation="vertical")
ax.legend(Temps)

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