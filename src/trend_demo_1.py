from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import numpy as np

pytrends = TrendReq(hl='en-US', tz=360)

### Single Keyword Data Retrieve and Plot
kw_list = ["Blockchain"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

# Obtain data (panda.DataFrame)
df = pytrends.interest_over_time()
np_list = df.values[:,:1].T[0]
print(np_list)

plt.plot(np_list)
plt.show()



### Multiple Keyword Data Retrieve and Plot
kw_list = ["S&P 500 Index", "Debt"]
pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')

# Obtain data (panda.DataFrame)
df = pytrends.interest_over_time()
df.T
np_list = df.T.values
print(np_list)
print(np_list.shape)
plt.plot(range(261), np_list[1], range(261), np_list[0])
