import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

#Import calculations.py
from calculations import cal_SOi, cal_NOi, cal_PMi, cal_RSPMi, cal_SPMi, cal_aqi, AQI_Range

# for model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier



with st.sidebar:
    choose = option_menu("Air Quality Index", ["About", "Data Analysis", "Data Visualization", "Prediction", "Conclusion"],
                         icons=['house', 'activity', 'bar-chart', 'alt','cloud-arrow-down'],
                         menu_icon="wind", default_index=0,
                         styles={
        # "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#grey"},
    }
    )

def get_data(filename):
    original_data = pd.read_csv(filename)
    return original_data
original_data = get_data("dataset.csv")

original_data.drop(['stn_code','agency','type','sampling_date','location_monitoring_station'],axis=1,inplace=True) 

# st.write(data.head(10))

data = original_data.copy()
#Mean distribution by state
state_mean_distribution = data.groupby('state')[['spm','pm2_5','rspm','so2','no2']].mean()

grp_state = data.groupby('state')

def fill_missing_by_mean(series):
    return series.fillna(series.mean()) 
data['rspm']=grp_state['rspm'].transform(fill_missing_by_mean)  #fill value with mean value group by state
data['so2']=grp_state['so2'].transform(fill_missing_by_mean)
data['no2']=grp_state['no2'].transform(fill_missing_by_mean)
data['spm']=grp_state['spm'].transform(fill_missing_by_mean)
data['pm2_5']=grp_state['pm2_5'].transform(fill_missing_by_mean)

# Creating an year column
data['date'] = pd.to_datetime(data['date'], format = '%m/%d/%Y')
data['year'] = data['date'].dt.year # year
data['year'] = data['year'].fillna(0.0).astype(int)
data = data[(data['year']>0)]

prediction_data = data.copy()
# Calculate sub-index,AQI, AQI range
   
prediction_data['SOi']=prediction_data['so2'].apply(cal_SOi)
prediction_data['NOi']=prediction_data['no2'].apply(cal_NOi)
prediction_data['RSPMi']=prediction_data['rspm'].apply(cal_RSPMi)
prediction_data['SPMi']=prediction_data['spm'].apply(cal_SPMi)
prediction_data['PMi']=prediction_data['pm2_5'].apply(cal_PMi)
prediction_data['AQI']=prediction_data.apply(lambda x:cal_aqi(x['SOi'],x['NOi'],x['RSPMi'],x['SPMi'],x['PMi']),axis=1)
prediction_data['AQI_Range'] = prediction_data['AQI'].apply(AQI_Range)

    # Drop rows with null values
prediction_data=prediction_data.dropna(subset=['spm']) #spm
prediction_data=prediction_data.dropna(subset=['pm2_5']) #pm2.5


# ------------------------------About section----------------------------------
if choose == "About":
    # To display the header text using css style
    st.markdown(""" <style> .font {
        font-size:35px ;  color: red;} 
        </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font">Indian Air Quality Index</p>', unsafe_allow_html=True)    
    
    st.subheader("What is AQI?")

    st.write("An air quality index or AQI is used by government agencies to communicate to the public how polluted the air currently is or how polluted it is forecast to become. Public health risks increase as the AQI rises. Different countries have their own air quality indices, corresponding to different national air quality standards")
    
    
    st.write('The purpose of the AQI is to help people know how the local air quality impacts their health.')
    

    st.markdown("""
    * **Pollutants(Features) that we are going to analyze and use for prediction:** 
        * **so2:** The amount of Sulphur Dioxide measured.
        * **no2:** The amount of Nitrogen Dioxide measured
        * **rspm:** Respirable Suspended Particulate Matter measured.
        * **spm:** Suspended Particulate Matter measured.
        * **pm2_5:** It represents the value of particulate matter measured.
    """)
    st.subheader("AQI Category")
    st.write('AQI can be divided into few category based on their AQI values. Each category has its own related to its impact on the envionment.')
    st.image('aqirange.jpg')

  

# ------------------------------Analysis section----------------------------------

elif choose == "Data Analysis":
    st.title('Data Analysis')
    st.write('''This dataset is related to Historical Daily Ambient Air Quality Data released by the 
    Ministry of Environment and Forests and Central Pollution Control Board of India 
    under the National Data Sharing and Accessibility Policy (NDSAP) year 1990-2015
    
    Here is data of first ten rows 

    ''')
    st.write(original_data.head(10))

    # data = get_data("dataset.csv")
    st.write('Total entries in the dataset(shape of the dataset)')
    entriess = original_data.shape
    st.write(entriess)
    st.subheader("Mean Distribution of data by state")
    st.write(state_mean_distribution)
    
    #filling missing values by mean

    st.subheader("Dataset Description")
    st.write("Dataset Description after replacing Null Values by mean value of the columns")

    st.write(data.describe())
    

# ------------------------------Visualization section----------------------------------
elif choose == "Data Visualization":

    st.title('Data Visualization')


    # plot correlation matrix 
    st.subheader('Correlation matrix between the independent variables')
    corrmat = data.corr()
    f, ax = plt.subplots(figsize = (15, 10))
    sns.heatmap(corrmat, vmax = 1, square = True, annot = True)
    st.write(f)

    st.header('Analyze pollutant through Heatmap')
    st.write('Shows the concentration of the pollutant in states in different years')

    pollutant = st.selectbox('Select pollutant',options= ['so2', 'no2', 'pm2_5','rspm', 'spm'], index = 0)

    # heatmap
    h, ax = plt.subplots(figsize = (10,10))
    ax.set_title('{} by state and year'.format(pollutant))
    sns.heatmap(data.pivot_table(pollutant, index = 'state',
                columns = ['year'], aggfunc = 'median', margins=True),
                annot = True, cmap = 'YlGnBu', linewidths = 1, ax = ax, cbar_kws = {'label': 'Average taken Annually'})
    st.write(h)

    


# ------------------------------Prediction section----------------------------------
elif choose == "Prediction":
    st.title('AQI Calulation and Prediction ')
    st.markdown("""

    To calculate AQI, minimum three parameters should be taken out of which one must be either PM10 or PM 2.5.
    To calculate sub-indices, 16 hours data is needed.
""")
    st.markdown("""
    * **Approach used**

        1. Calculate sub index(refered as si, ni, rspmi, spmi, pmi) of all pollutants using the formula.
        2. Find out max of all subindexes .
        3. Allot max as AQI.
        4. Classify AQI range corresponding to AQI value.
        5. Train model to predict and classify AQI range(Random forest classifier is used).
    """)


    
    st.subheader('Check AQI Here')
    # for User Input
    input_col, display_col= st.columns(2)
    input_so2 = input_col.text_input('Enter SO2 value')
    input_no2 = input_col.text_input('Enter NO2 value')
    input_rspm = input_col.text_input('Enter RSPM value')
    input_spm = input_col.text_input('Enter SPM value')
    input_pm2_5 = input_col.text_input('Enter PM2.5 Value')


    x = prediction_data[['so2','no2','rspm','spm','pm2_5']]
    y = prediction_data['AQI_Range']

    x_train, x_test, y_train, y_test = train_test_split(x,y,train_size = 0.8, test_size = 0.2, random_state=0)

  
    model = RandomForestClassifier(n_estimators=10)
    model.fit(x_train,y_train)

    if st.button('Predict'):
                
        accuracy = model.score(x_test,y_test)
        result= model.predict([[input_so2, input_no2, input_rspm, input_spm, input_pm2_5]])
        display_col.write('Predicted AQI Range is: ')
        display_col.write(result)

        display_col.write('With the model accuracy of : ')
        display_col.text(accuracy)


# ------------------------------Downloads section----------------------------------

elif choose == "Conclusion":
    st.subheader("Conclusion")
    st.write("""
        1. AQI is dependent on pollutant with the dominant value.
        2. AQI is highly correlated with all the independent variables(so2, no2, rspm, spm,pm2.5)
        3. By each year AQI kept worsening.
        
        * **Model Used:**
        Random Forest Classifier


        -View source code here:
        https://github.com/mauryapam/Air-Quality-Analysis-India

        
    """)
