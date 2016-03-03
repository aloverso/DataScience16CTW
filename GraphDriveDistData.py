import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kendalltau
import seaborn as sns

pd = pd.read_csv('../cities.csv')
pd = pd[pd.lng > -130]
driveTime = pd.drivetime
# lng = pd.lng
lat = pd.lat

x = lat
# x = lng
y = driveTime


plt.scatter(x, y, alpha=0.5)
plt.show()


# sns.set(style="ticks")

# rs = np.random.RandomState(11)
# x = rs.gamma(2, size=10)
# y = -.5 * x + rs.normal(size=1000)

# print x

# sns.jointplot(x, y, kind="hex", stat_func=kendalltau)
# , color="#4CB391"