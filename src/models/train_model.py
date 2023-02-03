import pathlib
import pandas as pd 
from statsmodels.tsa.arima.model import ARIMA

dirname = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()
df = pd.read_csv(str(dirname)+str("/data/raw/data.csv"),parse_dates=True, header=None)

df.columns = ['Datetime','Close']

history = [x for x in df['Close'].values]

modelF = ARIMA(history, order=(26,3,2))
model_Fit = modelF.fit()

model_Fit.save(str(dirname)+str("/models/model.pickle"))