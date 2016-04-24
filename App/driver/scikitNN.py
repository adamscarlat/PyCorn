from sknn.mlp import Classifier, Regressor, Layer
import driver
import numpy as np
import pickle
import matplotlib.pyplot as plt

config=driver.createConfigDictionary('configurations.txt')
table=driver.createTrainingTable(config)

print "table dimentions: ", table.shape

#our table
y = table[:,table.shape[1]-1]
x = table[:,0:table.shape[1]-1]

proportion = 75

trainCount = (table.shape[0] * proportion) / 100
testCount = table.shape[0] - trainCount

x_train, x_test = x[:trainCount,:], x[trainCount:,:]
y_train, y_test = y[:trainCount], y[trainCount:]

print x_train, 
print x_test,
print y_train,
print y_test

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

pipeline = Pipeline([
        ('min/max scaler', MinMaxScaler(feature_range=(0.0, 1.0))),
        ('neural network',  Classifier(layers=[Layer("Tanh", units=256), 
                                             Layer("Softmax", units=2)], n_iter=25, learning_rate=0.001, verbose=True))])
pipeline.fit(x_train, y_train)

y_test2 = pipeline.predict(x_test)

tpr=[0.0]
fpr=[0.0]

positives=float(np.count_nonzero(y_test))
negatives=float(len(y_test)-positives)

tpCount = 0
fpCount = 0
tnCount = 0
fnCount = 0
truePredictions = 0
for res in xrange(len(y_test2)):
	try:
		if y_test2[res] == y_test[res]:
			truePredictions += 1.0
		if y_test2[res] == 1 and y_test[res] == 1:
			tpCount += 1.0
		if y_test2[res] == 1 and y_test[res] == 0:
			fpCount += 1.0
		if y_test2[res] == 0 and y_test[res] == 1:
			fnCount += 1.0
		if y_test2[res] == 0 and y_test[res] == 0:
			tnCount += 1.0
	except:
		print "index error ",res

	tpr.append(tpCount/positives)
	fpr.append(fpCount/negatives)


print "validation rate: ", float(truePredictions/len(y_test2))
print "true positives: ", tpCount
print "false positives: ", fpCount
print "true negatives: ", tnCount
print "false negatives: ", fnCount
pickle.dump(pipeline, open('pipelineH.pkl', 'wb'))





