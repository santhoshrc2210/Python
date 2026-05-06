# Use the following data for this assignment:

import pandas as pd
import numpy as np

#By setting a "seed," you ensure that the sequence of random numbers generated is the same every time you run your code.
np.random.seed(12345)

#np.random.normal(x,y,z): x:mean, y: standard deviation, z: number of samples
df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df

#Your Code Here
import matplotlib.pyplot as plt

#plt.bar(df.index, df.mean(axis=1))
#plt.xlabel('Year')
#plt.xticks(df.index)

#print(df.loc[1992].mean())
#plt.hist(df.loc[1992], density=True, bins=20, color='skyblue',alpha=0.5)
df_means = pd.DataFrame()
df_means['means_1992'] = pd.DataFrame({'means_1992':[np.random.normal(32000,200000,3650).mean() for i in range(1000)]})
df_means['means_1993'] = pd.DataFrame({'means_1993':[np.random.normal(43000,100000,3650).mean() for i in range(1000)]})
df_means['means_1994'] = pd.DataFrame({'means_1994':[np.random.normal(43500,140000,3650).mean() for i in range(1000)]})
df_means['means_1995'] = pd.DataFrame({'means_1995':[np.random.normal(48000,70000,3650).mean() for i in range(1000)]})
#df_means.set_index(['means_1992','means_1993','means_1994','means_1995'])
#print(df_means.index)

#create lists for plot
x_pos = np.arange(len(df.index))
num= [df.loc[1992].mean(), df.loc[1993].mean(), df.loc[1994].mean(), df.loc[1995].mean()]
error=[df_means['means_1992'].std(), df_means['means_1993'].std(), df_means['means_1994'].std(), df_means['means_1995'].std()]
#build the plot
fig, ax = plt.subplots(figsize=(12, 12))
#So bars might be colored red if they are definitely above this value (given the confidence interval), 
#blue if they are definitely below this value, or white if they contain this value.

plt.axhline(y=42000, color='black', linestyle='--')
plt.text(x_pos[0], 48000, '-----:user provided y-axis value=42000', color='black', fontsize=12)

print(df.loc[1994].mean()+df_means['means_1994'].std())

#assume user provided value=42000
usr_y_val=42000
colors = []

for i in range(len(num)):
    if usr_y_val > num[i] + error[i]:
        colors.append('skyblue')
    elif usr_y_val < num[i] + error[i] and usr_y_val > num[i] - error[i]:
        colors.append('green')
    else:
        colors.append('red')
        
        

ax.bar(x_pos, num, yerr=error, align='center', alpha=1, ecolor='black', capsize=10, color=colors)
ax.set_xlabel('Year')
ax.set_ylabel('Random number mean')
ax.set_xticks(x_pos)
ax.set_xticklabels(df.index)
ax.set_title('Ferreira, N., Fisher, D., & Konig, A. C. (2014, April)')
#ax.yaxis.grid(True)

#label errorbars
for i, val in enumerate(num):
    # Position text slightly above the top of the error bar
    plt.text(x_pos[i], val + error[i] + 500, f'{num[i]+error[i]}', ha='center', color='purple')
    plt.text(x_pos[i], val - error[i] - 1000, f'{num[i]-error[i]}', ha='center', color='purple')
    
# Save the figure and show
#plt.tight_layout()
plt.savefig('bar_plot_with_error_bars.png')
plt.show()
