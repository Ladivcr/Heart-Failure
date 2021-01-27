#Cargamos las librerias que vamos a necesitar
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

# Cargamos los datos con los que vamos a trabajar
heart_failure = pd.read_csv('heart_failure_clinical_records_dataset.csv')

eval = heart_failure[['age','ejection_fraction','serum_creatinine','time', 'DEATH_EVENT']]

result = KMeans(n_clusters=5,init='random',max_iter=200).fit(eval.drop('DEATH_EVENT',axis=1))


cluster_result = list(result.labels_)
eval = eval.assign(Cluster_group = cluster_result)



#graficamos las 3 dimensiones mas importantes

X = np.array(eval[['ejection_fraction','serum_creatinine','time']])

labels=np.array(eval['Cluster_group'])
plt.style.use('classic')

y = np.array(eval['DEATH_EVENT'])

fig = plt.figure()
ax=Axes3D(fig)
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels,s=60)
plt.show()
