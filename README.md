# human help
   human interact data clustering tool

#This pacakge is only working on the Jupyter notebook.

## How to use

### Performance evaluation
0. Make a preprocessed dataset with [pandas](https://pandas.pydata.org) DataFrame type 
1. Make a clustering algorithm object from [sklearn](https://scikit-learn.org/stable/)
2. Call the 'clustering_evaluation(clustering_algorithm_object, dataset)'
3. Expected processing time for the chosen algorithm with dataset will return.

### Human interact clustering
0. Make a preprocessed dataset with [pandas](https://pandas.pydata.org) DataFrame type
   0-1. if the dataset has attributes more than 2, it will be compressed on two principles components as PCA method.
1. Type '%matplotlib notebook'
2. Make a object 'HumanClusteringInterface(dataset)'
3. Draw lines by clicking. ('c' key can delete the last clicked point)
4. Press the 'z' key. It makes a cluster as draw a line between the first point and the last point.
5. Make clusters as much as you want and after that Press the 'f' key.
6. object.result_df contain the clustering result and object.clustering_result() method can show it as a plot.