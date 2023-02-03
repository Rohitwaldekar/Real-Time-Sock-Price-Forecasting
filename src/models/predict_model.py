import pathlib
from statsmodels.iolib.smpickle import load_pickle

dirname = pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()
model = load_pickle(str(dirname)+str("/models/model.pickle"))

output = model.forecast(steps=7)

print('Output :', output)
