# Nothing here

import matplotlib.pyplot as plt
import seaborn as sns


def plot_missing(df):
    plt.figure(figsize=(10,5))
    sns.heatmap(df.isnull(), cbar=False)
    plt.show()

if __name__ == "__main__":
    pass