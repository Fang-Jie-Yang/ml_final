from libsvm.svmutil import *
import random as rand
from sklearn import metrics
from sklearn.model_selection import train_test_split
from svm_util import *
from imblearn.over_sampling import SMOTE

#### Data Processing ####
train_ids = []
x_train = []
y_train = []
read_data('train.csv', train_ids, x_train, y_train)
for i in range(len(y_train)):
	if y_train[i] > 0:
		y_train[i] = 1
for i in range(len(x_train)):
	x_train[i] = normalize(x_train[i])

#### Model Settings ####
x_res, y_res = SMOTE(random_state=1212).fit_resample(x_train, y_train)
for i in range(len(x_res)):
	print(y_res[i], end='')
	for j in range(len(x_res[i])):
		if x_res[i][j] != 0:
			print("", j, end='')
			print(":", end='')
			print(x_res[i][j], end='')
	print("")
