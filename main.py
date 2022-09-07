import time

start_time = time.time()
from pandas_ods_reader import read_ods

# task scriptini ekleme
from task import *

# ods dosyalarını okuma
mydata = read_ods("actdata.ods", "Sheet1")

# kiritik yolu hesaplama
mydata = computeCPM(mydata)


printTask(mydata)

#iş sayısı
ntask = mydata.shape[0]

# kritik yolu yazdırma
cp = []

for i in range(ntask):
    if(mydata['SLACK'][i]==0):
        cp.append(mydata['IS'][i])
print('Kritik Yol: ' + '-'.join(cp))

# projenin toplam süresini hesaplama
tdur = 0
for i in range(ntask):
    if(mydata['SLACK'][i]==0):
        tdur = tdur + mydata['GUN'][i]

print('Proje toplam suresi: ' + str(tdur) + ' unit time')