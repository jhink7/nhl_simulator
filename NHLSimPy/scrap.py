import numpy as np
import pandas as pd
s = np.random.poisson(5, 10000)


import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 14, normed=True)
#plt.show()


events = np.random.poisson(6, 10)
df = pd.DataFrame({'iat':events})
df['at'] = df['iat'].cumsum()

#print list(df['at'])

filtered  = [ num for num in list(df['at']) if num < 30 ]

print filtered