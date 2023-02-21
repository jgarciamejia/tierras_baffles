import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

# Load Data from Load Sensors in All Locations at all dates. Units: lbs 

# Dates and times 
dates = np.array(['2021-11-29', '2021-11-29', '2021-12-08', '2021-12-15',
                  '2021-12-20', '2021-12-22', '2022-01-02', '2022-01-10'])
dates = [datetime.strptime(val, "%Y-%m-%d") for val in dates]


# U = upper, L = lower, S = south, N = north, E = east, W = west
UN_snsr_rdgs = np.array([20.28, 20.26, 20.92, 19.78, 19.62, 19.91, 19.82,19.16]) 
US_snsr_rdgs = np.array([20.3, 20.28, 20.92, 19.78, 19.6, 19.91, 19.78, 19.14])
UE_snsr_rdgs = np.array([21.19, 21.16, 19.69, 18.7, 18.1, 18.03, 18.03,15.45])
UW_snsr_rdgs = np.array([21.05, 21.03, 19.55, 18.63, 18.03, 17.97, 17.97,15.37])

LN_snsr_rdgs = np.array([30.8, 30.8, 29.56, 28.75, 28.2, 28.37, 28.37, 25.18])
LS_snsr_rdgs = np.array([30.82, 30.82, 29.59, 28.77, 28.24, 28.42, 28.4, 25.24]) 
LE_snsr_rdgs = np.array([29.43, 29.41, 29.78, 28.53, 28.24, 28.31, 28.22, 27.98])
LW_snsr_rdgs = np.array([29.19, 29.15, 29.5, 28.2, 27.95, 28.02, 27.91, 27.73])
snsrs = np.array([UN_snsr_rdgs, US_snsr_rdgs, UE_snsr_rdgs, UW_snsr_rdgs, 
	     LN_snsr_rdgs, LS_snsr_rdgs, LE_snsr_rdgs, LW_snsr_rdgs])

# Plot Data 
fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.6, 0.75])
locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b',
		  '#e377c2','#7f7f7f','#bcbd22','#17becf','#1a55FF']
labels = ['Upper North','Upper South','Upper East','Upper West',
		  'Lower North','Lower South','Lower East','Lower West']
for i in range(len(snsrs)):
	ax.plot(dates, snsrs[i], marker='o', label=labels[i], color=colors[i])

ax.set_ylabel('Load Reading (Lbs)')
ax.set_xlabel('Date')
ax.set_title('Lab Load Sensor Readings vs. Time')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
#fig.savefig('loadchange_over_time.pdf')



