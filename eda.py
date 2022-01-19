import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

demographics = pd.read_csv('demographics_fixed.csv')
demographics = demographics.set_index('Customer ID')
services = pd.read_csv('services_fixed_one_hot.csv')
services = services.set_index('Customer ID')
satisfaction = pd.read_csv('satisfaction.csv')
satisfaction = satisfaction.set_index('Customer ID')

status = pd.read_csv('status.csv')
status = status.set_index('Customer ID')
churn = pd.get_dummies(status['Churn Category'])
status = status.drop('Churn Category', axis=1)
status = status.join(churn)


df = demographics.join(services)
df = df.join(satisfaction)
df = df.join(status)



'''
test = pd.read_csv('age_test.csv')
plt.figure(figsize=(10, 8))
sns.scatterplot(data=test, x="Age", y="Avg Monthly GB Download")
plt.show()
'''

feature_corr = df.corr()

indexing = {}
total = 0
for col in feature_corr.columns:
	indexing[total] = col
	total += 1


cor_list = []

high_pos_cor = []
mod_pos_cor = []
high_neg_cor = []
mod_neg_cor = []
for index, row in feature_corr.iterrows():
	cor = []
	for i in range(total):
		if index == indexing[i]:
			continue
		if row[indexing[i]] >= 0.7:
			high_pos_cor.append((row[indexing[i]], index, indexing[i]))
			cor.append((row[indexing[i]], indexing[i]))
		elif row[indexing[i]] >= 0.3:
			mod_pos_cor.append((row[indexing[i]], index, indexing[i]))
			cor.append((row[indexing[i]], indexing[i]))
		if row[indexing[i]] <= -0.7:
			high_neg_cor.append((row[indexing[i]], index, indexing[i]))
			cor.append((row[indexing[i]], indexing[i]))
		elif row[indexing[i]] <= -0.3:
			mod_neg_cor.append((row[indexing[i]], index, indexing[i]))
			cor.append((row[indexing[i]], indexing[i]))
	cor_list.append((index, cor))

'''
def remove_dupilcated(l):
	for rel in l:
		c, a, b = rel
		if (c, b,a) in l:
			l.remove((c, b,a))
remove_dupilcated(high_pos_cor)
remove_dupilcated(mod_pos_cor)
remove_dupilcated(high_neg_cor)
remove_dupilcated(mod_neg_cor)
'''

'''
print("-----------------------------")
print("Highly Positive Correlated:")
for relation in high_pos_cor:
	print('\t', end='')
	print('%.2f'%relation[0], end=' ')
	print((relation[1], relation[2]))
print("-----------------------------")
print("Moderately Positive Correlated:")
for relation in mod_pos_cor:
	print('\t', end='')
	print('%.2f'%relation[0], end=' ')
	print((relation[1], relation[2]))
print("-----------------------------")
print("Highly Negative Correlated:")
for relation in high_neg_cor:
	print('\t', end='')
	print('%.2f'%relation[0], end=' ')
	print((relation[1], relation[2]))
print("-----------------------------")
print("Moderately Negative Correlated:")
for relation in mod_neg_cor:
	print('\t', end='')
	print('%.2f'%relation[0], end=' ')
	print((relation[1], relation[2]))
print("-----------------------------")
'''

for index, cor in cor_list:
	print("----------------------------")
	print(f"\'{index}\'")
	for c in sorted(cor, key=lambda x: abs(x[0]), reverse=True):
		print('\t', end='')
		print('%.2f'%c[0], end=' ') 
		print(f"with \'{c[1]}\'")
