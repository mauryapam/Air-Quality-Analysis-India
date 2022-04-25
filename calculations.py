# 1. Calculate sub indices of all pollutant
# 2. AQI = max(all sub- indexes of pulltants)
# 3. Classify AQI into AQI range


#sub-index of SO(sulphur Oxide)
def cal_SOi(so2):
    si=0
    if (so2<=40):
        si= so2*(50/40)

    elif (so2>40 and so2<=80):
        si= 50+(so2-40)*(50/40)

    elif (so2>80 and so2<=380):
        si= 100+(so2-80)*(100/300)

    elif (so2>380 and so2<=800):
        si= 200+(so2-380)*(100/420)

    elif (so2>800 and so2<=1600):
        si= 300+(so2-800)*(100/800)

    elif (so2>1600):
        si= 400+(so2-1600)*(100/800)
    return si


# data['SOi']=data['so2'].apply(cal_SOi)
# df= data[['so2','SOi']]
# df.head(10)


#sub-index of NO(Nitrous Oxide)
def cal_NOi(no2):
    ni=0
    if(no2<=40):
     ni= no2*50/40
    elif(no2>40 and no2<=80):
     ni= 50+(no2-40)*(50/40)
    elif(no2>80 and no2<=180):
     ni= 100+(no2-80)*(100/100)
    elif(no2>180 and no2<=280):
     ni= 200+(no2-180)*(100/100)
    elif(no2>280 and no2<=400):
     ni= 300+(no2-280)*(100/120)
    else:
     ni= 400+(no2-400)*(100/120)
    return ni
# data['NOi']=data['no2'].apply(cal_Noi)
# df= data[['no2','Noi']]
# df.head()


#sub-index of RSPM -(respirable suspended particualte matter concentration)
def cal_RSPMi(rspm):
    rpi=0
    if(rspm<=100):
     rpi = rspm
    elif(rspm>=101 and rspm<=150):
     rpi= 101+(rspm-101)*((200-101)/(150-101))
    elif(rspm>=151 and rspm<=350):
     ni= 201+(rspm-151)*((300-201)/(350-151))
    elif(rspm>=351 and rspm<=420):
     ni= 301+(rspm-351)*((400-301)/(420-351))
    elif(rspm>420):
     ni= 401+(rspm-420)*((500-401)/(420-351))
    return rpi
# data['RSPMi']=data['rspm'].apply(cal_RSPMi)
# df= data[['rspm','RSPMi']]
# df.head()


#sub-index of SPM - suspended particulate matter
def cal_SPMi(spm):
    spi=0
    if(spm<=50):
     spi=spm*50/50
    elif(spm>50 and spm<=100):
     spi=50+(spm-50)*(50/50)
    elif(spm>100 and spm<=250):
     spi= 100+(spm-100)*(100/150)
    elif(spm>250 and spm<=350):
     spi=200+(spm-250)*(100/100)
    elif(spm>350 and spm<=430):
     spi=300+(spm-350)*(100/80)
    else:
     spi=400+(spm-430)*(100/430)
    return spi
   
# data['SPMi']=data['spm'].apply(cal_SPMi)
# df= data[['spm','SPMi']]
# df.head()


#sub-index of PM2.5
def cal_PMi(pm2_5):
    pmi=0
    if(pm2_5<=50):
     pmi=pm2_5*(50/50)
    elif(pm2_5>50 and pm2_5<=100):
     pmi=50+(pm2_5-50)*(50/50)
    elif(pm2_5>100 and pm2_5<=250):
     pmi= 100+(pm2_5-100)*(100/150)
    elif(pm2_5>250 and pm2_5<=350):
     pmi=200+(pm2_5-250)*(100/100)
    elif(pm2_5>350 and pm2_5<=450):
     pmi=300+(pm2_5-350)*(100/100)
    else:
     pmi=400+(pm2_5-430)*(100/80)
    return pmi
# data['PMi']=data['pm2_5'].apply(cal_pmi)
# df= data[['pm2_5','PMi']]
# df.head()



# calculate aqi 
def cal_aqi(si,ni,rspmi,spmi,pmi):
    aqi=0
    if(si>ni and si>rspmi and si>spmi and si>pmi):
     aqi=si
    elif(ni>si and ni>rspmi and ni>spmi and ni>pmi):
     aqi=ni
    elif(rspmi>si and rspmi>ni and rspmi>spmi and rspmi>pmi):
     aqi=rspmi
    elif(spmi>si and spmi>ni and spmi>rspmi and spmi>pmi):
     aqi=spmi
    elif(pmi>si and pmi>ni and pmi>rspmi and pmi>spmi):
     aqi=pmi
    return aqi

# data['AQI']=data.apply(lambda x:cal_aqi(x['SOi'],x['Noi'],x['RSPMi'],x['SPMi'],x['PMi']),axis=1)
# df= data[['state','SOi','Noi','RSPMi','SPMi','PMi','AQI']]
# df.head()

def AQI_Range(x):
    if x<=50:
        return "Good"
    elif x>50 and x<=100:
        return "Satisfactory"
    elif x>100 and x<=200:
        return "Moderate"
    elif x>200 and x<=300:
        return "Poor"
    elif x>300 and x<=400:
        return "Very Poor"
    else:
        return "Severe"

# data['AQI_Range'] = data['AQI'].apply(AQI_Range)
# data.head()

# data=data.dropna(subset=['spm']) #spm
# data=data.dropna(subset=['pm2_5']) #pm2.5



