# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:52:35 2020

@author: Nasser, Camille & Michael
"""

#importing librairies
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#defining functions:

#Functions to clean and collect data:

def data_collection(path):
    """collecting the dataframe from a folder"""
    return pd.read_csv(path)

def data_cleaning(df):
    """cleaning the data obtained"""
    df['Date']=df['dt_iso'].astype(str).str[:10]
    df["Date"]= pd.to_datetime(df['Date'])
    df['month'] = pd.DatetimeIndex(df['Date']).month
    df['year'] = pd.DatetimeIndex(df['Date']).year
    df["delta_T"] = df["temp_max"].subtract(df["temp_min"], fill_value=0)
    return df

def checking_delta(df):
    return df.loc[(df['delta_T'] < 0)]

def todecade(y): 
    return str(y)[2] + '0'

def rename_decade(df):
    df.decade=df.decade.str.replace('70','1970').str.replace('80','1980').str.replace('90','1990').str.replace('00','2000').str.replace('10','2010').str.replace('20','2020')
    df.decade=df.decade.str.replace('202010','2010').str.replace('202000','2000')
    return df

#Function to chose the city:
    
def df_city(city):
    if city == "Berlin":
        return df[df.city_name == 'Berlin']
    elif city == "Hotan":
        return df[df.city_name == 'Hotan Prefecture']
    elif city =="Milan":
        return df[df.city_name == 'Milan']


#Functions for data wrangling and data analysis:
        
def temp_decade(dfcity):
    df = dfcity.groupby(['decade']).mean().reset_index().drop(5).drop(0)
    return df

def plot_av_temp(df_decade):
    plot1 = df_decade.plot(kind='line',x='decade',y='temp')
    plt.title(f"Average temperature per decade for {city}")
    plt.xlabel('Decade')
    plt.ylabel('Average temperature')
    plt.show()
    return plot1

def temp_months_decade(dfcity):
    df=dfcity.groupby(['decade','month']).mean().reset_index()
    return df

def df2_create(df_months_decade):
    df=df_months_decade.drop(columns=['dt','timezone','lat','lon','temp_min','temp_max','feels_like','pressure','sea_level','grnd_level','humidity','wind_speed','wind_deg','rain_1h','rain_3h','snow_1h','snow_3h','clouds_all','weather_id','year','delta_T']).reset_index(drop=True).set_index(['month'])
    return df

def plot_temp_month(df_graph2):
    fig, ax = plt.subplots(1,1,figsize=(6, 4))
    for i, (j, col) in enumerate(df_graph2.iteritems()):
        col = col.rename_axis([None, None])
        plot2=col.unstack(fill_value=0).plot(ax=ax, legend=False)
        if i == 0:
            ax.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    fig.tight_layout()
    plt.xlabel('Months')
    plt.ylabel('Average temperature')
    st = plt.suptitle(f"Average temperature per month \n and per decade for {city}", fontsize=12)
    st.set_y(0.95)
    fig.subplots_adjust(top=0.75)
    plt.show()
    return plot2

def plot_delta(df_decade):
    plotdelta=df_decade.plot(kind='line',x='decade',y='delta_T')
    plt.title(f"Average delta per decade for {city}")
    plt.xlabel('Decade')
    plt.ylabel('Average temperature variation (delta T)')
    plt.show()
    return plotdelta

def df_plot3b(df_decade):
    df=df_decade.drop(columns=['dt','timezone','lat','lon','temp','feels_like','pressure','sea_level','grnd_level','humidity','wind_speed','wind_deg','rain_1h','rain_3h','snow_1h','snow_3h','clouds_all','weather_id','year','delta_T','month']).reset_index(drop=True).set_index(['decade'])
    return df

def plot_max_min_temp(df_graph3b):
    fig, ax = plt.subplots(1,1, figsize=(6, 5))
    for i, (j, col) in enumerate(df_graph3b.iteritems()):
        col = col.rename_axis([None, None])
        plot3b=col.unstack(fill_value=0).plot(ax=ax, legend=False)
        if i == 0:
            ax.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    plt.title(f"Average minimum and maximum temperature \n per decade for {city}")
    plt.xlabel('Decade')
    plt.ylabel('Temperature')
    plt.show()
    return plot3b

def df_plot4(dfcity):
    df=dfcity.groupby(['decade','month']).mean().drop(columns=['dt','timezone','lat','lon','temp','feels_like','pressure','sea_level','grnd_level','humidity','wind_speed','wind_deg','rain_1h','rain_3h','snow_1h','snow_3h','clouds_all','weather_id','year','delta_T']).reset_index().set_index(['month'])
    return df

def plot_max_min_month(df_graph4):
    fig, axes = plt.subplots(1, 4, figsize=(15, 4))
    for i, (j, col) in enumerate(df_graph4.iteritems()):
        ax = axes[i]
        col = col.rename_axis([None, None])
        plot4=col.unstack(fill_value=0).plot(ax=ax, title=j, legend=False)
        ax.xaxis.set_major_locator(plt.MaxNLocator(13))
        ax.set_xlabel('Months')
        ax.set_ylabel('Temperature')
        if i == 0:
            ax.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    fig.tight_layout()
    st = plt.suptitle(f'Average minimum and maximum temperature per month and per decade for {city}', fontsize="x-large")
    st.set_y(0.95)
    fig.subplots_adjust(top=0.75)
    plt.show()
    return plot4

def df5(dfcity):
    """Checking covid impact on recent temperatures"""
    df=dfcity.groupby(['decade','month']).mean().reset_index().drop(columns=['dt','timezone','lat','lon','temp_min','temp_max','feels_like','pressure','sea_level','grnd_level','humidity','wind_speed','wind_deg','rain_1h','rain_3h','snow_1h','snow_3h','clouds_all','weather_id','year','delta_T'])
    return df.loc[(df.month == 1) | (df.month == 2) | (df.month == 3)]

def plot_impact_covid(df_graph5):
    fig, ax = plt.subplots(1,1,figsize=(7, 6))
    for i, (j, col) in enumerate(df_graph5.iteritems()):
        col = col.rename_axis([None, None])
        plot5=col.unstack(fill_value=0).plot(ax=ax, legend=False)
        if i == 0:
            ax.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    fig.tight_layout()
    plt.xlabel('Months')
    plt.ylabel('Average temperature')
    #plt.title(f"Average temperature per decade \n for January, February and March in {city}")
    st=plt.suptitle(f"Average temperature per decade \n for January, February and March in {city}", fontsize=12)
    st.set_y(0.85)
    fig.subplots_adjust(top=0.75)
    plt.locator_params(axis='x', nbins=3)
    plt.show()
    return plot5

def plot_correlation(dfcity_corr):
    plt.figure(figsize=(20, 20))
    p = sns.heatmap(dfcity_corr.corr(), annot=True, square=True)
    st=plt.suptitle(f"Correlation between temperature parameters for {city}", fontsize=16)
    st.set_y(0.85)
    plt.show()
    return p

# functions to export results:
def save_viz(barchart,title,path_output):
    """saving the graphs"""
    os.chdir(path_output)
    fig = barchart.get_figure()
    fig.savefig(title+ '.png')
    plt.show()
    
def save_clean_df(df,path_output):
    """saving the dataframe into a csv"""
    os.chdir(path_output)
    df.to_csv('Clean_meteo_dataframe.csv')

def save_clean_df_city(dfcity, path_output):
    """saving the dataframe into a csv"""
    os.chdir(path_output)
    dfcity.to_csv(f'Clean_meteo_dataframe for {city}.csv')

#Calling functions:
if __name__ == '__main__':
    
    #define where to get the csv and where to save the output:
    path='C:/Users/Camille/Documents/Ecole/Ironhack/Week 4/Group project/Data_weather.csv'
    path_output='C:/Users/Camille/Documents/Ecole/Ironhack/Weather_Analysis_Project/Group project/Output'
    
    #choose the city to analyse between Milan Berlin and Hotan
    city="Berlin"
    
    #data cleaning
    df=data_collection(path)
    df=data_cleaning(df)
    data_cleaning(df)
    df["decade"] = df["year"].apply(todecade)
    df=rename_decade(df)
    
    #data wrangling per city chosen
    dfcity=df_city(city)
    dfcity.reset_index(drop=True)
    
    #data analysis:
    
    #analysis of average temperature per decade
    df_decade=temp_decade(dfcity)
    plot1=plot_av_temp(df_decade)
    
    #average temperature per month per decade
    df_months_decade=temp_months_decade(dfcity)
    df2=df2_create(df_months_decade)
    df_graph2=pd.pivot_table(df2, values=['temp'], index=['decade'],columns=['month','decade'], aggfunc=np.mean, fill_value=0).T.reset_index().set_index(["month","level_0"]).drop(columns=["1970","2020"])
    df_graph2["value"]=df_graph2["1980"]+df_graph2["1990"]+df_graph2["2000"]+df_graph2["2010"]
    df_graph2=df_graph2.drop(columns=["1980","1990","2000","2010"])
    df_graph2=df_graph2[(df_graph2.decade != "1970")&(df_graph2.decade != "2020")]
    df_graph2=df_graph2.reset_index().set_index(["month","decade"], drop=False).drop(columns=["month","level_0","decade"])
    plot2=plot_temp_month(df_graph2)

    #average variation of temperature per decade
    plot3=plot_delta(df_decade)
    df_decade.groupby('decade')["delta_T"].mean()
    
    #min and max temperatures per decade
    df3b=df_plot3b(df_decade)
    df_graph3b=pd.pivot_table(df3b, values=['temp_min','temp_max'], columns=['decade'], index=["decade"],aggfunc=np.mean, fill_value=0).T.reset_index().set_index(["decade","level_0"])
    df_graph3b["value"]=df_graph3b["1980"]+df_graph3b["1990"]+df_graph3b["2000"]+df_graph3b["2010"]
    df_graph3b=df_graph3b.drop(columns=["1980","1990","2000","2010"])
    plot3b=plot_max_min_temp(df_graph3b)
    
    #min and max temperature per month per decade
    df4=df_plot4(dfcity)
    df_graph4=pd.pivot_table(df4, values=['temp_min','temp_max'], index=['decade'],columns=['month'], aggfunc=np.mean, fill_value=0).T.reset_index().set_index(["month","level_0"]).drop(columns=["1970","2020"])
    plot4=plot_max_min_month(df_graph4)
    
    #checking Covid impact on recent temperatures
    df_Covid=df5(dfcity)
    df_Covid=df_Covid.set_index(['month'])
    df_graph5=pd.pivot_table(df_Covid, values=['temp'], index=['decade'],columns=['month','decade'], aggfunc=np.mean, fill_value=0).T.reset_index().set_index(["month","level_0"]).drop(columns=["1970"])
    df_graph5["value"]=df_graph5["1980"]+df_graph5["1990"]+df_graph5["2000"]+df_graph5["2010"]+df_graph5["2020"]
    df_graph5=df_graph5.drop(columns=["1980","1990","2000","2010","2020"])
    df_graph5=df_graph5[(df_graph5.decade != "1970")]
    df_graph5=df_graph5.reset_index().set_index(["month","decade"], drop=False).drop(columns=["month","level_0","decade"])
    plot5=plot_impact_covid(df_graph5)
    
    #checking any correlation between parameters and temperature
    dfcity_corr=dfcity.drop(columns=['sea_level','grnd_level','lat','lon','wind_deg','timezone','weather_id','clouds_all','rain_1h','rain_3h','snow_1h','snow_3h','year','month','dt'])
    plot6=plot_correlation(dfcity_corr)
    dfcorr=dfcity_corr.corr()
    
    #saving all graphs
    save_viz(plot1,f'1. Average temperature per decade for {city}',path_output)
    save_viz(plot2,f'2. Average temperature per month per decade for {city}',path_output)
    save_viz(plot3,f'3. Average variation of temperature per decade for {city}',path_output)
    save_viz(plot3b,f'3b. Average minimum and maximum temperature per decade for {city}',path_output)
    save_viz(plot4,f'4. Average minimum and maximum temperature per month and per decade for {city}',path_output)
    save_viz(plot5,f'5. Average temperature per month per decade for {city}',path_output)
    save_viz(plot6,f'6. Correlation matrix for {city}',path_output)
    
    #saving dataframes
    save_clean_df(df,path_output)
    save_clean_df_city(dfcity, path_output)
    print("Thanks for running the analysis. All files are saved in your output folder")