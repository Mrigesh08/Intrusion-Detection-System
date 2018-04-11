import xmeans as xmeans
import pythonarr2 as data
from sklearn.cluster import KMeans
import numpy as np


datap=np.array(data.arr)


def collectiveAnomalyDetection(datap):
	k=xmeans.xmeans(datap)
	kmeans=KMeans(n_clusters=k,init="k-means++",max_iter=300).fit(datap)

	centers = kmeans.cluster_centers_
	labels = kmeans.labels_
	m = kmeans.n_clusters
	n = np.bincount(labels)
	clusterDatapoints=[]
	for i in range(m):
		newDataPoints1=datap[np.where(labels==i)]
		# create an array of the payload length attribute
		newDataPoints2 = np.array([newDataPoints1[x][2] for x in range(len(newDataPoints1))])
		newDataPoints = newDataPoints2.reshape(-1,1)
		k2=xmeans.xmeans(newDataPoints)
		kmeans2 = KMeans(n_clusters=k2,init="k-means++",max_iter=300).fit(newDataPoints)
		# centers2 = kmeans2.cluster_centers_
		labels2 = kmeans2.labels_
		m2=kmeans2.n_clusters
		n2=np.bincount(labels)
		minVariance = 99999999999
		minVarianceClusterIndex = -1
		for j in range(m2):
			# calculate variance of each of the clusters. and record the label of the cluster with the least variance
			dataPoints = newDataPoints2[np.where(labels2 == j)]
			newVar = np.var(dataPoints)
			if newVar < minVariance:
				minVariance = newVar
				minVarianceClusterIndex = j
		print("Potential DOS attack Detected with records as follows")
		print(newDataPoints1[np.where(labels2 == minVarianceClusterIndex)])

collectiveAnomalyDetection(datap)