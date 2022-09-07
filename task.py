import numpy as np

def stars(number):
    for i in range(number):
        print("*", end ="")
    print("")

#hata
def errorCodeMsg():
    print("Error in input file: CODE")
    quit()

def errorPredMsg():
    print("Error in input file: ONCEKI ISLER")
    quit()

def errorDaysMsg():
    print("Error in input file: DAYS")
    quit()

# önceki iş ve sonraki iş verileri task kodundaki listede var mı sorgusu
def getTaskCode(mydata, code):
    x=0
    flag=0
    for i in mydata['IS']:
        if(i== code):
            flag=1
            break

        x+=1

    if(flag==1):
        return x
    else:
        errorCodeMsg()



# CPM EF ve ES hesaplama
# EF -> earliest finish
# ES -> earliest start
def forwardPass(mydata):
    ntask = mydata.shape[0]
    ES = np.zeros(ntask, dtype = np.int8)
    EF = np.zeros(ntask, dtype = np.int8)
    temp=[] #geçici

    for i in range(ntask):
        if(mydata['ONCEKI ISLER'][i] == None):
            ES[i] = 0
            try:
                EF[i] = ES[i] + mydata['GUN'][i]
            except:
                errorDaysMsg()
        else:
            for j in mydata['ONCEKI ISLER'][i]:
                index = getTaskCode(mydata, j)
                temp.append(EF[index])

                if(index==i):
                    errorPredMsg()
                else:
                    temp.append(EF[index])
            
            ES[i] = max(temp)
            try:
                EF[i] = ES[i] + mydata['GUN'][i]
            except:
                errorDaysMsg()

        #reset temp
        temp = []
    
    #ES ve EF update
    mydata['ES'] = ES
    mydata['EF'] = EF

    return mydata

#CPM LS ve LF hesaplama
#LS-> latest start
#LF-> latest finish
def backwardPass(mydata):
    ntask = mydata.shape[0]
    temp = []
    LS = np.zeros(ntask, dtype = np.int8)
    LF = np.zeros(ntask, dtype = np.int8)
    SUCCESSORS = np.empty(ntask, dtype = object)

    #Sonraki iş sütununu oluşturma(Successor)
    for i in range(ntask-1, -1, -1):
        if(mydata['ONCEKI ISLER'][i] != None):
            for j in mydata['ONCEKI ISLER'][i]:
                index = getTaskCode(mydata, j)
                if(SUCCESSORS[index] != None):
                    SUCCESSORS[index] += mydata['IS'][i]
                else:
                    SUCCESSORS[index] = mydata['IS'][i]

    #Sonraki is sütununa ekleme 
    mydata["SONRAKI IS"] = SUCCESSORS

    #LS = LF-D hesaplaması
    for i in range(ntask-1, -1, -1):
        if(mydata['SONRAKI IS'][i] == None):
            LF[i] = np.max(mydata['EF'])
            LS[i] = LF[i] - mydata['GUN'][i]
        else:
            for j in mydata['SONRAKI IS'][i]:
                index= getTaskCode(mydata, j)
                temp.append(LS[index])

            LF[i] = min(temp)
            LS[i] = LF[i] - mydata['GUN'][i]

            #reset temp
            temp=[]

    #LS ve LF update
    mydata['LS'] = LS
    mydata['LF'] = LF

    return mydata

#slack ve critical sütunları hesaplama
def slack(mydata):
    ntask= mydata.shape[0]

    SLACK = np.zeros(shape = ntask, dtype = np.int8)
    CRITICAL = np.empty(shape = ntask, dtype = object)

    for i in range(ntask):
        SLACK[i] = mydata['LS'][i] - mydata['ES'][i]
        if(SLACK[i]==0):
            CRITICAL[i] = "YES"
        else:
            CRITICAL[i] = "NO"
         
    #slack ve critical update
    mydata['SLACK'] = SLACK
    mydata['CRITICAL'] = CRITICAL

    #sütunları tekrar düzenleme
    mydata = mydata.reindex(columns = ['ACIKLAMA', 'IS', 'ONCEKI ISLER', 'SONRAKI IS', 'GUN', 'ES', 'EF', 'LS', 'LF', 'SLACK', 'CRITICAL'])

    return mydata

# kritik yolu hesaplayan fonksiyon
def computeCPM(mydata):
    mydata = forwardPass(mydata)
    mydata = backwardPass(mydata)
    mydata = slack(mydata)
    return mydata
    

# print fonk
def printTask(mydata):
    print("KRITIK YOL ALGORITMASI")
    stars(90)
    print("ES= earliest start; EF= earliest finish; LS= latest start; LF= latest finish")
    stars(90)
    print(mydata)
    stars(90)