import pandas as pd

# reduced
d_red = pd.read_csv("2d_classification.csv")
print("REDUCED shape:", d_red.shape)
print(d_red.groupby("N").size().sort_values(ascending=False).head(10))

# full (whatever the file is called — probably a _full.csv or the
# 103,427-row export referenced in results-1)
d_full = pd.read_csv("2d_classification_full.csv")   # adjust name
print("FULL shape:", d_full.shape)
print(d_full.groupby("N").size().sort_values(ascending=False).head(10))
