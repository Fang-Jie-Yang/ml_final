from libsvm.svmutil import *
import random as rand
from sklearn import metrics
from sklearn.model_selection import train_test_split
from svm_util import *
from imblearn.over_sampling import SMOTE
import numpy as np
import matplotlib.pyplot as plt

#### Data Processing ####
train_ids = []
X = []
y = []
x_train = []
y_train = []
read_data('train.csv', train_ids, X, y)
for i in range(len(y)):
    if y[i] > 0:
        y_train.append(y[i])
        x_train.append(X[i])
for i in range(len(x_train)):
    x_train[i] = normalize(x_train[i])
print(len(x_train) // 5)
exit()

#### Grid Search ####
def f1_score(y_test, y_pred):
    return metrics.classification_report(y_test, y_pred, output_dict=True, zero_division=0)['macro avg']['f1-score']

best_score = 0
c_list = [2**(i) for i in range(-10, 10)]
gamma_list = [2**(i) for i in range(-10, 10)]
sc_arr = np.ndarray([len(gamma_list), len(c_list)])
print(sc_arr)
for i in range(len(gamma_list)):
    gamma = gamma_list[i]
    for j in range(len(c_list)):
        c = c_list[j]
        option = f"-s 0 -t 2 -c {c} -g {gamma} -q"
        avg_score = 0
        for t in range(5):
            #### Create Test/Train Sets ####
            x_tr, x_val, y_tr, y_val = train_test_split(x_train, y_train, test_size=0.2)
            x_res, y_res = SMOTE().fit_resample(x_tr, y_tr)
            prob = svm_problem(y_res, x_res)
            m = svm_train(prob, option)
            y_pred, acc, vals = svm_predict(y_val, x_val, m)
            y_pred = [int(i) for i in y_pred]
            avg_score += f1_score(y_val, y_pred)
        score = avg_score / 5
        print(f"C: {c}, gamma: {gamma}, score: {score}")
        sc_arr[i][j] = score
        if score > best_score:
            best_score = score
            best_parameters = {'gamma': gamma, 'C': c}
print(best_parameters, best_score)
print(sc_arr)
plt.imshow(sc_arr, interpolation='none')
plt.show()
