from sklearn.cluster import KMeans
from scipy.spatial import distance
import numpy as np
import plotly as py
import plotly.graph_objs as go

d=4 # number of dimensions/features to be clustered

def calculateBIC(datapoints, k, centers):
	# datapoints is a 3-d array of datapoints of 'k' clusters
	# 'centers' a 2d array of cluster centers
	global d
	N=0
	for i in range(len(datapoints)):
		N=N+datapoints[i].shape[0]
	
	# don't split clusters of size less than 3
	if N<3:
		return 999999999

	x=[datapoints[i].shape[0] for i in range(k)] # number of points in each cluster
	const_term = 0.5 * k * np.log(N) * (d+1)
	var = (1.0/((N-k)*d)) * np.sum([np.sum(distance.cdist(datapoints[i],np.array([centers[i]]),'euclidean') ** 2) for i in range(k)])
	BIC = np.sum([x[i]*np.log(x[i]) - x[i]*np.log(N) - (N*d)*0.5*np.log(2*np.pi*var) - d*0.5*(x[i]-1) for i  in range(k)]) - const_term
	return BIC

def xmeans(datapoints):
	bestBIC = -1
	bestBICNumberOfCluster =1
	KMAX=int((datapoints.shape[0]/2)**0.5)
	k=2 # starting number of clusters 
	while k<KMAX:
		# Improve params
		kmeans = KMeans(n_clusters =k,init="k-means++",max_iter=300).fit(datapoints)
		centers = [kmeans.cluster_centers_]
		labels = kmeans.labels_
		m = kmeans.n_clusters
		n = np.bincount(labels)

		dArray = np.array([datapoints[np.where(labels == i)] for i in range(m)])
		newBIC = abs(calculateBIC(dArray,m,centers[0]))
		if newBIC > bestBIC:
			bestBIC = newBIC
			bestBICNumberOfCluster = k
		
		# Improve Structure
		# split each cluster into two and calculate BIC
		flag =0
		for i in range(m):
			if k < KMAX:
				newdataset=datapoints[np.where(labels==i)]
				if newdataset.shape[0]>2:
					# print("calculating BIC for %d number of records",newdataset.shape[0])
					BICone=abs(calculateBIC([newdataset], 1, centers[0]))

					kmeans2=KMeans(n_clusters = 2,init="k-means++",max_iter=1000).fit(newdataset)
					newLabels=kmeans2.labels_
					newCenters = [kmeans2.cluster_centers_]
					BICtwo=abs(calculateBIC([newdataset[np.where(newLabels==0)],newdataset[np.where(newLabels==1)]], 2,newCenters[0] ))
					
					if np.isnan(BICtwo):
						return bestBICNumberOfCluster
					# print("BICtwo=",BICtwo, " BICone=",BICone)
					if BICtwo > BICone:
						flag=1
						k=k+1
		if flag==0:
			k=k+1
						
	# print("FINAL NUMBER OF CLUSTERS=",bestBICNumberOfCluster)
	return bestBICNumberOfCluster

def plot(datapoints, centers):
	trace = go.Scatter3d(
			x=np.array([datapoints[i][0] for i in range(datapoints.shape[0])]),
			y=np.array([datapoints[i][1] for i in range(datapoints.shape[0])]),
			z=np.array([datapoints[i][2] for i in range(datapoints.shape[0])]),
			mode='markers'
		)
	trace1 = go.Scatter3d(
			x=np.array([centers[i][0] for i in range(centers.shape[0])]),
			y=np.array([centers[i][1] for i in range(centers.shape[0])]),
			z=np.array([centers[i][2] for i in range(centers.shape[0])]),
			mode='markers'
		)
	data=[trace,trace1]
	fig=go.Figure(data=data)
	py.offline.plot(fig)
	print("PLOT GENERATED")

# plot(datap)
# k=xmeans(datap)
# finalAnswer = KMeans(n_clusters=k,init="k-means++",max_iter=300).fit(datap)
# centers = finalAnswer.cluster_centers_

# plot(datap, centers)