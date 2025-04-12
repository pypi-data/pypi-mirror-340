import matplotlib.pyplot as plt

def plot_histograms(df):
    num_features = df.select_dtypes(include='number').columns
    n = len(num_features)
    cols = 3
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = axes.flatten()
    for i, col in enumerate(num_features):
        df[col].hist(ax=axes[i], bins=20, edgecolor='black')
        axes[i].set_title(col)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    plt.tight_layout()
    return fig