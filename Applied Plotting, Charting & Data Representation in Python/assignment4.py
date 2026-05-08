import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib as mpl


#load data
df_vk = pd.read_csv('readonly/kohli_stats_subset.csv')
#print(df_vk.head())

df_sr = pd.read_csv('readonly/sachin_perfomance.csv')
#print(df_sr.head())

df_msd = pd.read_excel('readonly/msdData (1).xlsx')
#print(df_msd.head())

df_rs = pd.read_excel('readonly/rohitsharmaodi.xlsx')
#print(df_rs.head())

#data cleaning

df_vk[['Runs scored', 'Balls played']] = df_vk['Run'].str.split(' ', expand=True)
df_vk[['Runs scored', 'SR']] = df_vk[['Runs scored', 'SR']].astype(float)
#print(df_vk['Runs scored'])

#df_sr = df_sr[~df_sr['runs'].str.contains('-', na=False)]
df_sr = df_sr[~df_sr['SR'].str.contains('-', na=False)]
df_sr[['runs', 'SR']] = df_sr[['runs', 'SR']].astype(float)

df_msd = df_msd[~df_msd['S/R'].str.contains('-', na=False)]
df_msd[['Runs', 'S/R']] = df_msd[['Runs', 'S/R']].astype(float)
#print(df_msd.shape)

df_rs = df_rs[~df_rs['SR'].str.contains('-', na=False)]
df_rs[['Runs', 'SR']] = df_rs[['Runs', 'SR']].astype(float)

#print(df_vk.head())

#plotting data
#set figure size
plt.figure(figsize=(20, 8))

plt.subplot(2, 2, 1)
plt.yticks(np.arange(0, 201, 20))
plt.title("Virat Kohli")
plt.ylabel('Runs Scored')
plt.xlabel('Strike Rate')

colors = ['red','green','blue']
cmap = mcolors.ListedColormap(colors)
bounds = [0, 50, 100, 200] 
norm = mcolors.BoundaryNorm(bounds, cmap.N)
plt.scatter(df_vk['SR'], df_vk['Runs scored'], c=df_vk['Runs scored'], marker='.', alpha=0.5, cmap=cmap, norm=norm);
# Add colorbar
plt.colorbar(ticks=bounds, label='Runs Scored')



plt.subplot(2, 2, 2)
plt.yticks(np.arange(0, 250, 30))
bounds = [0, 50, 100, 250] 
norm = mcolors.BoundaryNorm(bounds, cmap.N)
plt.scatter(df_sr['SR'], df_sr['runs'], c=df_sr['runs'], marker='.', alpha=0.5, cmap=cmap, norm=norm);
plt.title("Sachin Tendulkar")
plt.ylabel('Runs Scored')
plt.xlabel('Strike Rate')
plt.colorbar(ticks=bounds, label='Runs Scored')


plt.subplot(2, 2, 3)
plt.yticks(np.arange(0, 201, 20))
bounds = [0, 50, 100, 200] 
norm = mcolors.BoundaryNorm(bounds, cmap.N)
plt.scatter(df_msd['S/R'], df_msd['Runs'], c=df_msd['Runs'], marker='.', alpha=0.5, cmap=cmap, norm=norm);
plt.title("M S Dhoni")
plt.ylabel('Runs Scored')
plt.xlabel('Strike Rate')
plt.colorbar(ticks=bounds, label='Runs Scored')

plt.subplot(2, 2, 4)
plt.yticks(np.arange(0, 275, 30))
bounds = [0, 50, 100, 275] 
norm = mcolors.BoundaryNorm(bounds, cmap.N)
plt.scatter(df_rs['SR'], df_rs['Runs'], c=df_rs['Runs'], marker='.', alpha=0.5, cmap=cmap, norm=norm);
plt.title("Rohit Sharma")
plt.ylabel('Runs Scored')
plt.xlabel('Strike Rate')
plt.colorbar(ticks=bounds, label='Runs Scored')
#print(df_rs['Runs'].max())

#title for all subplots
plt.suptitle('Strike Rate vs Runs: ODI batsmen from India', fontsize=12)
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.4)
