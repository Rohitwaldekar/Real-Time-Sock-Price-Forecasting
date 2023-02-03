import pathlib
import numpy as np 
import pandas as pd 
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA

import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import pacf, acf
from statsmodels.graphics.tsaplots import plot_acf
dirname = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()
df = pd.read_csv(str(dirname)+str("/data/raw/data.csv"),parse_dates=True, header=None)
df.columns = ['Datetime','Close']

dif = df['Close']
for i in range(1,10):
    dif = dif.diff().dropna()
    result = acf(dif)
    print(i,result)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))

    ax1.plot(dif)
    ax1.set_title('Difference once')
<<<<<<< HEAD
    plot_acf(dif, ax=ax2);
=======
    plot_acf(dif, ax=ax2);
>>>>>>> 18e32c82e73716b910bd5eee3fc47b9a3f754ddc
