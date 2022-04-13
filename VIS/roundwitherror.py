from math import *
import xlrd
import numpy as np

def getData(path):
    content=""
    with open (path)as f:
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

def round_err(num, err,  sig=2):
    posof1digit = floor(log10(abs(err)))
    rnum = round(num, sig-int(floor(log10(abs(err))))-1)
    srnum = str(rnum)
    if posof1digit <= 0:
        abrerr = err*10**(-int(floor(log10(abs(err))))+1)
        while len(srnum.split('.')[1]) <= -posof1digit:
            srnum += '0'
    
    else:
        abrerr = round(err, sig-int(floor(log10(abs(err))))-1)
        srnum = str(int(rnum))
    

    return(srnum + '(' + str(ceil(abrerr)) + ')')

def getAxis(row1,collumn1,row2,path,sheet):
    data = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    for i in range(row1,row2):
        data.append(worksheet.cell(i, collumn1).value)    
    return data

def getRow(collumn1,row1,collumn2,path,sheet):
    data = []
    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_name(sheet)
    for i in range(collumn1,collumn2):
        data.append(worksheet.cell(row1, i).value)    
    return np.array(data)



def FehlerFort(part1,part2,err1,err2,vals):
    return np.sqrt(part1(vals)**2*err1**2+part2(vals)**2*err2**2)

def arrToString(arr):
    string="["
    for i,I in enumerate(arr):
        if i !=len(arr)-1:
            string+=str(I)+","
        else:
            string+=str(I) +"]"
    return string

def genDataFromFunktion(amount,von,bis,params,func):
    x=[]
    y=[]
    for i in range(amount+1):
        x.append(von+i*(bis-von)/amount)
    for i in range(amount+1):
        y.append(func(x[i],params))

    return x,y

def getPlotable(rData):
    data=[[],[]]
    for i,I in enumerate(rData):
        data[0].append(I[0])
        data[1].append(I[1])
    return data

def getDataVonBis(path,von,bis):
    content=""
    with open (path)as f:
        content = f.read().replace(",",".")
        
    buf = content.split("\n")
    content=[]
    for i,I in enumerate(buf):
        if(von<=i and i<bis):
            buffer=I.split("\t")
            buffer2=[]
            for N in buffer:
                
                buffer2.append(float(N))
            content.append(buffer2)
    return content

def wichtungsFaktor(err):
    return 1/err**2
def gewichteterMittelwert(vals,errs):
    buf =0
    for i in range(len(vals)):
        buf+= vals[i]*wichtungsFaktor(errs[i])
    buf2 =0 
    for i in range(len(vals)):
        buf2+= wichtungsFaktor(errs[i])
    return buf/buf2
def internerFehler(errs):
    buf=0
    for i in range(len(errs)):
        buf+=wichtungsFaktor(errs[i])
    return np.sqrt(1/buf)
def externerFehler(vals,errs):
    buf1=0
    gewAvg = gewichteterMittelwert(vals,errs)
    for i in range(len(vals)):
        buf1+=wichtungsFaktor(errs[i])*(vals[i]-gewAvg)**2
    buf2 =0
    for i in range(len(vals)):
        buf2+= wichtungsFaktor(errs[i])
    return np.sqrt(buf1/((len(vals)-1)*buf2))
    
def intExtFehler(errs,vals):
    return max(internerFehler(errs),externerFehler(vals,errs))

def cut(xy):
    for i, I in enumerate(xy[1]):
        if xy[1][i] <= 0 and xy[1][i+1] >=0:
            ind = i
            break
    for i in range(ind):
        now = xy[1][i]
        if -100 < now < -70 and xy[1][i+1] >  -70:
            n = i
            break
    return(n)
