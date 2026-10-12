import pandas as pd
import matplotlib.pyplot as plt

path = "data.csv"
df = pd.read_csv(path)
df["score_num"] = pd.to_numeric(df["score"].replace("-", pd.NA), errors="coerce")
print("shape:", df.shape)
print("dtypes:\n", df.dtypes)
print("missing values:\n", df.isna().sum())
print("placeholder counts:\n", (df == "-").sum())
print("category counts:\n", df["category"].value_counts(dropna=False))
print("province counts:\n", df["province"].value_counts().head(15))
print("score summary:\n", df["score_num"].describe())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
df["province"].value_counts().head(15).sort_values().plot.barh(ax=axes[0], title="Universities by province (top 15)")
df.boxplot(column="score_num", by="category", ax=axes[1], grid=False)
axes[1].set_title("Score distribution by category")
axes[1].set_xlabel("Category")
plt.suptitle("")
plt.tight_layout()
plt.savefig("eda_overview.png", dpi=160)
