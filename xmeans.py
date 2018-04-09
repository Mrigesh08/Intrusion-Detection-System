import pythonarr2 as data
from sklearn.cluster import KMeans
from scipy.spatial import distance
import numpy as np
import plotly as py
import plotly.graph_objs as go
from plotly import __version__

# py.offline.init_notebook_mode()
print(__version__)

datap = np.array(data.arr)
print(datap.shape[0])
KMAX = int((datap.shape[0]/2)**0.5)
print("KMAX = ",KMAX)
d=4


def calculateBIC(datapoints, k, centers):
	# datapoints is a 3-d array of datapoints of 'k' clusters
	# 'centers' an array of cluster centers
	# print("CALCULATING BIC")
	global d
	# print(len(datapoints))
	# print(datapoints[0][0])
	if k==1:
		N=datapoints[0].shape[0]
	elif k==2:
		N=datapoints[0].shape[0]+datapoints[1].shape[0]
	
	if N==k:
		return 999999999

	x=[datapoints[i].shape[0] for i in range(k)]
	# print(x)
	# print(N)
	const_term = 0.5 * k * np.log(N) * (d+1)
	var = (1.0/((N-k)*d)) * sum([sum(distance.cdist(datapoints[i],np.array([centers[i]]),'euclidean') ** 2) for i in range(k)])
	BIC = np.sum([x[i]*np.log(x[i]) - x[i]*np.log(N) - (N*d)*0.5*np.log(2*np.pi*var) - d*0.5*(x[i]-1) for i  in range(k)]) - const_term
	return BIC

def xmeans(datapoints):
	k=2 # starting number of clusters 
	while k<KMAX:
		# Improve params
		kmeans = KMeans(n_clusters =k,init="k-means++",max_iter=300).fit(datapoints)

		# Improve Structure
		# split each cluster into two and calculate BIC
		centers = [kmeans.cluster_centers_]

		labels = kmeans.labels_
		m = kmeans.n_clusters
		n = np.bincount(labels)
		print("NEW NUMBER OF CLUSTERS=",m)
		# print("number of clusters ",m)
		# print("cluster centers",centers)
		# bic=calculateBIC([datapoints[np.where(labels==0)]], 1, centers[0])
		# print(bic)
		# # k=k+1
		for i in range(m):
			if k < KMAX:
				newdataset=datapoints[np.where(labels==i)]
				if newdataset.shape[0]>1:
					BICone=abs(calculateBIC([newdataset], 1, centers[0]))

					kmeans2=KMeans(n_clusters = 2,init="k-means++",max_iter=300).fit(newdataset)
					newLabels=kmeans2.labels_
					newCenters = [kmeans2.cluster_centers_]
					BICtwo=abs(calculateBIC([newdataset[np.where(newLabels==0)],newdataset[np.where(newLabels==1)]], 2,newCenters[0] ))
					
					print("BICtwo=",BICtwo, " BICone=",BICone)
					if BICtwo > BICone:
						k=k+1
	print("FINAL NUMBER OF CLUSTERS=",k)
	# this k probably wrong
	return k

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
k=xmeans(datap)
finalAnswer = KMeans(n_clusters=k,init="k-means++",max_iter=300).fit(datap)
centers = finalAnswer.cluster_centers_

plot(datap, centers)