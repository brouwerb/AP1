from pickletools import optimize
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib as mpl
from scipy import optimize
import math

X_START =0
Y_START =0
X_END = 1.7
Y_END = 2.5
TITEL = "Ordnung der Maxima in Bezug zur Röhrenlänge"
Y_LABEL = r"Dämpfungskonstante $\lambda$"
X_LABEL = r"Stromstäre in Wirbelstrombremse in $A$"
X_ERROR = 4
Y_ERROR = 1
X_MAJOR_TICK = 0.5
Y_MAJOR_TICK =0.5
X_MINOR_TICK =0.1
Y_MINOR_TICK = 0.1
SAVE_AS = "./POR/6Plot.pdf"
POINT_STYLE = ["o","^","s"]
COLOR_STYLE =["blue","red","green"]

Fits = [[[154.73762436048682,0.054849598148885875,3.1244232702381853,1.1237581053180126],[1.1906612521705262,0.000592763399204044,0.0006032663507882536,0.007959084129265772]],
        [[154.06736169609215,0.0976611030188857,3.1189030986975985,1.6705252524059255],[0.9030079316745859,0.0007720520228019844,0.000769605919820482,0.005809387722812539]],
        [[170.13702766589137,0.15730574337486858,3.1132535829739156,6.512355833013279],[0.8674664779521798,0.000976957584033556,0.0009789145848029602,0.005092613100903107]],
        [[151.73675851164128,0.23333744669494982,3.1033208715415923,2.585950190456993],[0.48975802557397086,0.0011018852083055101,0.0011862314447617598,0.003722834872722351]],
        [[168.07790999122776,0.33413142667857243,3.088093440723531,1.7919778383794045],[0.5545392151292429,0.0013305956145231058,0.0013606825061372098,0.0033807009684542868]],
        [[213.020716663584,0.4398206873769744,3.067804559130612,6.6759730055131685],[0.6776219502470506,0.0015133300014171433,0.0017370609777783515,0.004078417858929789]],
        [[226.41162418809674,0.5627287239985566,3.097942740691568,6.746199999999998],[2.065890765261605,0.004888053347870577,0.005636702963130184,0.011452384089130338]],
        [[196.0310030652458,0.7096034899707016,2.98232703423731,1.7963411830032212],[0.7933172780371239,0.0038828377049788133,0.0047294183324168935,0.006202418714617093]],
        [[221.5315662413464,0.8611120207219007,2.9423666652131306,1.5778706251561552],[0.8765780226390761,0.003522411503545466,0.004654092488409345,0.0062600834021884315]],
        [[197.89592666934797,1.0302340126925784,2.8910017312650864,2.0784164695636957],[0.7250538117159945,0.005264451147023591,0.006889985553048954,0.006835843432172548]],
        [[455.61741683142964,1.2296041339111183,2.8215497259623334,0.2947010683673322],[3.5994598042781285,0.006726008302795229,0.008119454195382028,0.011919347124249545]],
        [[708.6957999999998,1.429859926596756,2.7531237629103837,6.097415340856622],[7.338739252343618,0.007825952680400577,0.00905219281605659,0.014637138131361664]],
        [[191.73865182443848,1.7041179204817645,2.633596782770586,2.3745193959617974],[0.8521530387775128,0.01099087950372315,0.012157060578385998,0.008964106999388531]],
        [[377.92709976757686,1.982152282052107,2.461560076112558,1.5691163856944284],[4.569282886184451,0.017717065521522902,0.01108242854735838,0.010568144485445742]]
         ]


def xErr(x):
    return np.sqrt(((0.025* x)/np.sqrt(3))**2 + 0.0101/3)
def quotientArray(oben,unten):
    buf=[]
    for i in range(len(oben)):
        buf.append(float(oben[i])/float(unten[i]))
    return buf

def partOben(vals):
    return 1/vals[1]
def partUnten(vals):
    return -1*vals[0]/vals[1]**2

def FehlerFort(part1,part2,err1,err2,vals):
    return np.sqrt(float(part1(vals)**2*err1**2+part2(vals)**2*err2**2))


def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y
def Parabel(x,k):
    return k* x**2





x=[(i+2)*0.1 for i in range(len(Fits))]
y =[Fits[i][0][1] for i in range(len(Fits))]
errorsY =[Fits[i][1][1] for i in range(len(Fits))]
errorsX = [xErr(x[i]) for i in range(len(x))]
popt,perr = optimize.curve_fit(Parabel,x,y,sigma=errorsY)
print(popt,perr)

xy =genDataFromFunktion(1000,X_START,X_END,popt[0],Parabel)


#test

plt.style.use("./AKU/AP1_style.mplstyle")



fig, ax = plt.subplots()
ax.grid()
sc=[[],[],[]]
theo =[[],[],[]]

    
sc = ax.errorbar(x, y,fmt=".",yerr = errorsY,xerr=errorsX, ecolor = 'black',elinewidth=0.8,capsize=2,capthick=0.8,
    color=COLOR_STYLE[0])
#sc=ax.scatter(x,y,marker=POINT_STYLE[0],color=COLOR_STYLE[0],s=8,linewidths=1,edgecolors="black",zorder=10)
theo,=ax.plot(xy[0],xy[1],color= COLOR_STYLE[1],linestyle="dotted")
ax.legend([sc, theo],[r"Dämpfungskonstante $\lambda$ mit Fehler",r"Theoriekurve $\lambda=\kappa*I^2$ mit $\kappa=$0.89653(30)"])
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

