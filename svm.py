from libsvm.svmutil import *
from sklearn import metrics
from sklearn.model_selection import train_test_split
from svm_util import *
from imblearn.over_sampling import SMOTE

#### Data Processing ####
train_ids = []
X = []
y = []
read_data('train.csv', train_ids, X, y)
for i in range(len(X)):
	X[i] = normalize(X[i])
X_1_train = []
y_1_train = []
for i in range(len(y)):
	X_1_train.append(X[i])
	if y[i] == 0:
		y_1_train.append(0)
	else:
		y_1_train.append(1)
X_2_train = []
y_2_train = []
for i in range(len(y)):
    if y[i] > 0:
        X_2_train.append(X[i])
        y_2_train.append(y[i])

test_ids = []
X_test = []
y_test = []
read_data('test.csv', test_ids, X_test, y_test)
for i in range(len(X_test)):
	X_test[i] = normalize(X_test[i])

#### Model Settings ####
X_1_res, y_1_res = SMOTE(random_state=1212).fit_resample(X_1_train, y_1_train)
prob_1 = svm_problem(y_1_res, X_1_res)
option_1 = "-s 0 -t 2 -c 16384 -g 16 -q"
m_1 = svm_train(prob_1, option_1)

X_2_res, y_2_res = SMOTE(random_state=1212).fit_resample(X_2_train, y_2_train)
prob_2 = svm_problem(y_2_res, X_2_res)
option_2 = "-s 0 -t 2 -c 16 -g 0.5 -q"
m_2 = svm_train(prob_2, option_2)

#### Prediction ####
def model_predict(X_test):
	y_pred = []
	for i in range(len(X_test)):
		label, acc, val = svm_predict([], [X_test[i]], m_1, '-q')
		label = label[0]
		if label == 0:
			y_pred.append(0)
		else:
			label, acc, val = svm_predict([], [X_test[i]], m_2, '-q')
			label = label[0]
			y_pred.append(int(label))
	return y_pred

y_pred = model_predict(X)
print(metrics.classification_report(y, y_pred))

y_test_pred = model_predict(X_test)
out_dict = {}
for i in range(len(test_ids)):
	out_dict[test_ids[i]] = y_test_pred[i]
	
outfile = open("svm_pred.csv", "w")
with open('sample_submission.csv') as f:
	lines = f.readlines()
outfile.write(lines.pop(0))
for i in range(len(lines)):
	parts = lines[i].rstrip().split(',')
	ID = parts.pop(0)
	outfile.write(f"{ID},{out_dict[ID]}\n")
