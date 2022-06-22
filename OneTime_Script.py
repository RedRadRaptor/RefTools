import pickle
import pandas as pd

df = pd.read_csv(r"C:\Users\TaylorSe\Python Projects\Refrigerant Systems\Danfoss Valves(CSV).csv")
df.to_pickle("404A_DanEEVs.pkl")
file = open(r"C:\Users\TaylorSe\Python Projects\Refrigerant Systems\404A_DanEEVs.pkl", "wb")
pickle.dump(df, file)
file.close()