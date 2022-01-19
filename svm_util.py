import numpy as np
status_dict = {	'No Churn':			0, 
				'Competitor':		1,
				'Dissatisfaction':	2, 
				'Attitude':			3,
				'Price':			4,
				'Other':			5 }

def read_data(filename, ids, x, y):
	with open(filename) as f:
		lines = f.readlines()
	lines.pop(0)
	for line in lines:
		parts = line.rstrip().split(',')
		ID = parts.pop(0)
		label = parts.pop(-1)
		label = -1 if label == '' else status_dict[label]
		feature = [float(i) for i in parts]
		ids.append(ID)
		x.append(feature)
		y.append(label)
	return

def avg_f1_score(y_test, y_pred):
	tp = [0, 0, 0, 0, 0, 0]
	fp = [0, 0, 0, 0, 0, 0]
	fn = [0, 0, 0, 0, 0, 0]
	for i in range(len(y_test)):
		label = int(y_pred[i])
		if label == int(y_test[i]):
			# tp +1 for that label
			tp[label] += 1
		else:
			# fn +1 for correct label
			fn[y_test[i]] += 1
			# fp +1 for wrong prediction label
			fp[label] += 1
	f1_score_sum = 0
	for i in range(6):
		if tp[i] == 0:
			precision = 0
			recall = 0
		else:
			precision = tp[i] / (tp[i] + fp[i])
			recall = tp[i] / (tp[i] + fn[i])
		if not (precision == 0 and recall == 0):
			f1_score_sum += 2 * precision * recall / (precision + recall)
	return f1_score_sum / 6

def normalize(x):
	s = 0
	for x_i in x:
		s += x_i**2
	s = np.sqrt(s)
	return [x_i / s for x_i in x]


