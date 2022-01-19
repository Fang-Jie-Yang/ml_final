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


#### Create Test/Train Sets ####
x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2, random_state=1212)

#### Model Settings ####
x_res, y_res = SMOTE(random_state=1212).fit_resample(x_train, y_train)
prob = svm_problem(y_res, x_res)
option = "-s 0 -t 2"
'''
cnt = 0
for i in range(len(y_train)):
	if y_train[i] == 0:
		cnt += 1
w0 = 1 / cnt
w1 = 1 / (len(y_train) - cnt)
option += f" -w0 {w0} -w1 {w1}"
'''
m = svm_train(prob, option)

#### Testing ####
y_pred, acc, vals = svm_predict(y_test, x_test, m)
y_pred = [int(i) for i in y_pred]
print(metrics.classification_report(y_test, y_pred))
