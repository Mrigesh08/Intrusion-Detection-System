import xmeans as xmeans
import pythonarr2 as data
from sklearn.cluster import KMeans
import numpy as np


datap=np.array(data.arr)

def collectiveAnomalyDetection(datap):
	k=xmeans.xmeans(datap)
	kmeans=KMeans(n_clusters=k,init="k-means++",max_iter=300).fit(datap)

	centers = kmeans.cluster_centers_
	xmeans.plot(datap,centers)
	labels = kmeans.labels_
	print(labels)
	m = kmeans.n_clusters
	n = np.bincount(labels)
	print(n)
	clusterDatapoints=[]
	# minIndex=np.argmin(n)
	# print("minIndex=",minIndex," value=",n[minIndex], " min=",min(n))
	for i in range(m):
		newDataPoints=datap[np.where(labels==i)]
		k2=xmeans.xmeans2(newDataPoints)
		kmeans2 = KMeans(n_clusters=k2,init="k-means++",max_iter=300).fit(newDataPoints)
		centers2 = kmeans2.cluster_centers_

collectiveAnomalyDetection(datap)