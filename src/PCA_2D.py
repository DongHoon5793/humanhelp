from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd


def return_two_components_transformed(in_data):
    pca = PCA(n_components=2)

    scaler = StandardScaler()
    std_data = scaler.fit_transform(in_data)
    pca_data = pca.fit_transform(std_data)

    pca_data_frame = pd.DataFrame(pca_data, columns=[f'PC{i}' for i in range(1, 3)])
    return pca_data_frame
