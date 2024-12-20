import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from matplotlib.pyplot import xlabel
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler


def run_tsne_analysis(x, perplexity=30, scale=False, return_df=False):
    """
    Function to run t-SNE on array-like `x`.
    :param x: array-like to apply t-SNE on.
    :param perplexity: int from 5 to 50 affecting the nature of clusters being searched for -
        low values (closer to 5) mean a local search for clusters,
        high values (close to 50) mean a more global search for structure.
    :param scale: bool whether to scale `x` before t-sne
    :param return_df: bool determining whether a numpy array is returned or a dataframe is.
        To return a dataframe, the input must also be a dataframe (as it's index is used).
    :return: embeddings generated from running the t-SNE.
    """
    if scale:
        x_scaled = StandardScaler().fit_transform(x)
    else:
        x_scaled = x

    x_embedded = TSNE(perplexity=perplexity).fit_transform(x_scaled)

    if return_df:
        x_embedded = pd.DataFrame(x_embedded, index=x.index)

    return x_embedded


def plot_clusters(df, not_nominated=[], lost=[], won=[], target=[], x_col=0, y_col=1,
                  cs=None, alphas=None, title='clustering'):
    if alphas is None:
        alphas = [0.03, 0.6, 0.6]
    if cs is None:
        cs = ['tab:red', 'tab:blue', 'tab:green']
    if len(not_nominated) == 0:
        #         not_nominated = df.loc[df['oscar_nominated'] != True].index
        not_nominated = target.loc[target == 'not nominated'].index
    if len(lost) == 0:
        #         lost = df.loc[(df['oscar_nominated'] == True) & (df['winner'] == False)].index
        lost = target.loc[target == 'nominated but lost'].index
    if len(won) == 0:
        #         won = df.loc[(df['oscar_nominated'] == True) & (df['winner'] == True)].index
        won = target.loc[target == 'won oscar'].index

    labels = [not_nominated, lost, won]

    fig, ax = plt.subplots()
    ax.set_title(title)

    for i in range(3):
        ax.scatter(x=df.loc[labels[i], x_col], y=df.loc[labels[i], y_col], c=cs[i], alpha=alphas[i])

    #     ax.scatter(x=df.loc[:, x_col], y=df.loc[:, y_col], c=target, alpha=0.1)
    plt.legend(['not nominated for oscar', 'nominated but lost', 'won oscar'])
    plt.xlabel('Embedding 1')
    plt.ylabel('Embedding 2')
    plt.show()


def run_pca_analysis(x, n_components=None, normalize=True):
    if normalize:
        x_n = StandardScaler().fit_transform(x)
    else:
        x_n = x

    pca = PCA(n_components)
    x_decomposed = pca.fit_transform(x_n)

    return x_decomposed, pca


def pca_heatmap(pca_out, df, scale_by_evr=False, num_components=None, vmin=None, vmax=None, round=0, title=None):
    loadings = pca_out.components_
    if num_components is not None:
        num_pc=num_components
    else:
        num_pc = pca_out.n_features_in_
    pc_list = ["PC" + str(i) for i in list(range(1, num_pc + 1))]
    loadings_df = pd.DataFrame.from_dict(dict(zip(pc_list, loadings)))
    loadings_df['features'] = df.columns.values
    loadings_df = loadings_df.set_index('features')

    if scale_by_evr:
        loadings_df = loadings_df.mul(pca_out.explained_variance_ratio_)

    if round:
        loadings_df = loadings_df.round(round)
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(loadings_df, annot=True, cmap='Spectral', vmin=vmin, vmax=vmax, linewidth=0.5)
    if title is None:
        title = 'correlation of features with the principle components, weighted by explained-variance-ratio = {}'.format(scale_by_evr)
    ax.set_title(title)
    plt.show()

def elbow_plot(pca_out):
    evr = pca_out.explained_variance_ratio_
#     cvr = np.cumsum(pca_out.explained_variance_ratio_)
    plt.plot(range(1, len(evr) + 1), evr)
    plt.xlabel('Components')
    plt.ylabel('Explained Variance')
    plt.title('Elbow Plot')
    plt.show()

def pca_scatter_plot(pca_res, target):
    pca_res_df=pd.DataFrame(pca_res[:, 0:2], index=target.index, columns=['PC1', 'PC2'])
    pca_res_df['target']=target

    sns.lmplot(
        x='PC1',
        y='PC2',
        data=pca_res_df,
        hue='target',
        palette={'not nominated':'red', 'nominated but lost':'blue', 'won oscar':'green'},
        fit_reg=False,
        legend=True
    )

    plt.title('2D PCA Graph')
    plt.show()

def make_targets(nom, win):
    """
    Helper for making a 'target' feature
    :param nom: bool whether actor was nominated (for this movie)
    :param win: bool whether actor won an oscar (for this movie)
    :return: one of the values 'not nominated', 'nominated but lost' or 'won oscar'
    """
    if not nom:
        return 'not nominated'
    elif not win:
        return 'nominated but lost'
    else:
        return 'won oscar'

def get_top_n_columns_by_sum(df, n=10):
  """
  Helper to get the top N(=10) columns of a DataFrame based on their sum.
  :param df: The input DataFrame.
  :param n: The number of top columns to return.
  :return: list of the top N column names.
  """

  column_sums = df.sum()
  top_n_columns = column_sums.nlargest(n).index.tolist()
  return top_n_columns