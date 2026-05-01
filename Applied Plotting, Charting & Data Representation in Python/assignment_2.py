import pandas as pd
df = pd.read_csv('assets/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df.head()

# In this code cell, transform the Data_Value column
#transform the data into Celsius
df['Data_Value'] = df['Data_Value'].apply(lambda x: (x-32)/1.8)
#df.head()
#then extract all of the rows which have minimum or maximum temperatures
df_TMIN= df
df_TMIN = df[df['Element'] == 'TMIN']

df_TMAX= df
df_TMAX = df[df['Element'] == 'TMAX']

#print(df_TMAX.shape)
#print(df_TMIN.shape)

#unique_values = df_TMAX['Date'].unique()
#print(len(unique_values))

#drop records for Feb 29
df_TMAX = df_TMAX[~df_TMAX['Date'].str.contains(r'\d{4}-02-29', na=False)]
df_TMIN = df_TMIN[~df_TMIN['Date'].str.contains(r'\d{4}-02-29', na=False)]
#print(df_TMAX.shape)
#print(df_TMIN.shape)
# create a DataFrame of maximum temperature by date
series_TMAX=df_TMAX.groupby('Date').agg(['max'])
#print(series_TMAX.head())
# create a DataFrame of minimum temperatures by date
series_TMIN=df_TMIN.groupby('Date').agg(['min'])
#print(series_TMIN)


#seperate out data for 2015
series_TMAX_2015=series_TMAX[series_TMAX.index.str.match(r'2015-\d{2}-\d{2}')]
#print(series_TMAX_2015)
series_TMIN_2015=series_TMIN[series_TMIN.index.str.match(r'2015-\d{2}-\d{2}')]
#print(series_TMIN_2015)

# calculate the minimum and maximum values for the day of the year for 2005 through 2014
df_TMAX = pd.DataFrame(series_TMAX)
df_TMAX.columns = ['ID', 'Element', 'Data_Value']
df_TMAX = df_TMAX[~df_TMAX.index.str.contains(r'2015-\d{2}-\d{2}', na=False)]
#print(df_TMAX)
df_TMAX['Date'] = df_TMAX.index
df_TMAX_05to14 = df_TMAX[['Date', 'ID', 'Element','Data_Value']].reset_index(drop=True)
df_TMAX_day=df_TMAX_05to14.groupby(df_TMAX_05to14['Date'].str[5:]).max()
#print(df_TMAX_day.head(10))


df_TMIN = pd.DataFrame(series_TMIN)
df_TMIN.columns = ['ID', 'Element', 'Data_Value']
df_TMIN = df_TMIN[~df_TMIN.index.str.contains(r'2015-\d{2}-\d{2}', na=False)]
#print(df_TMIN.tail())
df_TMIN['Date'] = df_TMIN.index
df_TMIN_05to14 = df_TMIN[['Date', 'ID', 'Element','Data_Value']].reset_index(drop=True)
df_TMIN_day=df_TMIN_05to14.groupby(df_TMIN_05to14['Date'].str[5:]).min()
#print(df_TMIN_05to14.groupby(df_TMIN_05to14['Date'].str[5:]).get_group('01-01'))
#print(df_TMIN_day.head(10))


# calculate the minimum and maximum values for the years 2015
df_TMAX_2015 = pd.DataFrame(series_TMAX_2015)
df_TMAX_2015.columns = ['ID', 'Element', 'Data_Value']
df_TMAX_2015['Date'] = df_TMAX_2015.index
df_TMAX_15 = df_TMAX_2015[['Date', 'ID', 'Element','Data_Value']].reset_index(drop=True)
#print(df_TMAX_15)

df_TMIN_2015 = pd.DataFrame(series_TMIN_2015)
df_TMIN_2015.columns = ['ID', 'Element', 'Data_Value']
df_TMIN_2015['Date'] = df_TMIN_2015.index
df_TMIN_15 = df_TMIN_2015[['Date', 'ID', 'Element','Data_Value']].reset_index(drop=True)
#print(df_TMIN_15)

import matplotlib.pyplot as plt
from calendar import month_abbr

# put your plotting code here!
plt.rcParams['xtick.labelsize'] = 150
plt.rcParams['ytick.labelsize'] = 150


#print(df_TMAX_day)
lst_xlabels=[]
for date in df_TMAX_day['Date']:
    #print(date)
    if date[-2:] == '15':
        #print(date)
        #print(month_abbr[int(date[5:7])])
        lst_xlabels.append(month_abbr[int(date[5:7])])
    else:
        lst_xlabels.append('')
        
plt.figure(figsize=(365, 100))
plt.plot(df_TMAX_day['Date'],df_TMAX_day['Data_Value'], label="Maximum daily temparature from 2005-2014", lw=20)
plt.plot(df_TMAX_day['Date'],df_TMIN_day['Data_Value'], label="Minimum daily temparature from 2005-2014", lw=20)

plt.xticks(df_TMAX_day['Date'], lst_xlabels)

ax = plt.gca()
ax.set_xlabel('Month', fontsize=300)
ax.set_ylabel('Temperature (Celsius)', fontsize=300)
ax.set_title("Comparison of daily Temperature Variation: 2015 vs past decade", fontsize=300)
  


plt.gca().fill_between(df_TMAX_day['Date'], 
                       df_TMAX_day['Data_Value'], df_TMIN_day['Data_Value'], 
                       facecolor='green', 
                       alpha=0.1)

#scatter plot only the daily 2015 temperatures that exceeded those values

#print(df_TMAX_15.head(10))
df_TMAX=df_TMAX_day[['Date', 'ID', 'Element','Data_Value']].reset_index(drop=True)
#print(df_TMAX.head(10))

df_TMAX_15['Data_Value gt']= df_TMAX_15['Data_Value'] - df_TMAX['Data_Value']
df_TMAX_15_gt=df_TMAX_15[df_TMAX_15['Data_Value gt'] > 0]
#replace 2015 by 2014 to match x-cordinates
df_TMAX_15_gt['Date'] = df_TMAX_15_gt['Date'].astype(str)
df_TMAX_15_gt['Date'] = df_TMAX_15_gt['Date'].str.replace('2015', '2014', regex=False)

#print(df_TMAX_15_gt['Date'].dtype)
#print(df_TMAX_15_gt)

plt.scatter(df_TMAX_15_gt['Date'], df_TMAX_15_gt['Data_Value'], color='red', marker='x', s=5000, linewidths=20, label='temp in 2015 above that over past decade')


df_TMIN=df_TMIN_day[['Date', 'ID', 'Element','Data_Value']].reset_index(drop=True)
#print(df_TMIN.head(10))
#print(df_TMIN_15)
df_TMIN_15['Data_Value lt']= df_TMIN_15['Data_Value'] - df_TMIN['Data_Value']
df_TMIN_15_lt=df_TMIN_15[df_TMIN_15['Data_Value lt'] < 0]
df_TMIN_15_lt['Date'] = df_TMIN_15_lt['Date'].astype(str)
df_TMIN_15_lt['Date'] = df_TMIN_15_lt['Date'].str.replace('2015', '2014', regex=False)

plt.scatter(df_TMIN_15_lt['Date'], df_TMIN_15_lt['Data_Value'], color='green', marker='x', s=5000, linewidths=20, label='temp in 2015 below that over past decade')

plt.legend(fontsize=150)













