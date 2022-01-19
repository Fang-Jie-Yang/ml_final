import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler

def knn_impute(df, related_list, n_neighbors):
	imputed_df = df[related_list]
	scaler = MinMaxScaler()
	imputer = KNNImputer(n_neighbors=n_neighbors)
	imputed_df = pd.DataFrame(scaler.fit_transform(imputed_df), columns=imputed_df.columns)
	imputed_df = pd.DataFrame(imputer.fit_transform(imputed_df), columns=imputed_df.columns)
	imputed_df = pd.DataFrame(scaler.inverse_transform(imputed_df), columns=imputed_df.columns)
	print(imputed_df)
	for col in related_list:
		df[col] = imputed_df[col].values

def half_round(x):
	if x >= 0.5:
		return 1
	else:
		return 0

def binary_round(df, li):
	for i in df.index:
		for col in li:
			if df.at[i, col] != np.nan:
				df.at[i, col] = half_round(df.at[i, col])
def int_round(df, li):
	for i in df.index:
		for col in li:
			if df.at[i, col] != np.nan:
				df.at[i, col] = round(df.at[i, col])


# Merge CSVs

ids = pd.read_csv('Train_IDs.csv')['Customer ID'].tolist()
train_ids = pd.read_csv('Train_IDs.csv')['Customer ID'].tolist()
test_ids = pd.read_csv('Test_IDs.csv')['Customer ID'].tolist()
ids.extend(test_ids)
	
df = pd.DataFrame(ids, columns=['Customer ID']).set_index('Customer ID')
demographics = pd.read_csv('demographics_fixed.csv').set_index('Customer ID')
services = pd.read_csv('services_fixed_one_hot.csv').set_index('Customer ID')
satisfaction = pd.read_csv('satisfaction.csv').set_index('Customer ID')
df = df.join(demographics)
df = df.join(services)
df = df.join(satisfaction)
cnt = 0
for index, row in df.iterrows():
	if index in train_ids:
		if row.isna().sum() >= 15:
			cnt += 1
			df = df.drop(index)
print("drop", cnt, "rows")


# Drop Gender(Hard to impute)
df = df.drop('Gender', axis = 1)

# Age, Under 30, Senior Citizen, Avg Monthly GB Download are related
cor_list = [	'Age',
				'Under 30',
				'Senior Citizen',
				'Avg Monthly GB Download'	]
int_list = [	'Age',
				'Avg Monthly GB Download'	]
knn_impute(df, cor_list, 10)
# Drop Under 30, Senior Citizen
df = df.drop(['Under 30', 'Senior Citizen'], axis=1)
int_round(df, int_list)


# Married, Referred a Friend are HIGHLY correlated
for i in df.index:
	# Married -> Referral
	if not df.isna().at[i, 'Married']:
		if df.at[i, 'Married'] == 0:
			df.at[i, 'Referred a Friend'] = 0
			df.at[i, 'Number of Referrals'] = 0
		else:
			df.at[i, 'Referred a Friend'] = 1
	# Referral -> Married
	if not df.isna().at[i, 'Referred a Friend']:
		df.at[i, 'Married'] = df.at[i, 'Referred a Friend']

# Married, Referred a Friend, Number of Referrals, Dependents, Number of Dependents are related
cor_list =  [	'Married',
				'Referred a Friend', 
				'Number of Referrals', 
				'Dependents', 
				'Number of Dependents'	]
bin_list = [	'Married',
				'Referred a Friend', 
				'Dependents'	]
int_list =  [	'Number of Referrals', 
				'Number of Dependents'	]

knn_impute(df, cor_list, 10)
binary_round(df, bin_list)
int_round(df, int_list)


cor_list =  [	'Monthly Charge',
				'Internet Service',
				'DSL',
				'Cable',
				'Fiber Optic',
				'Streaming TV',
				'Streaming Movies',
				'Unlimited Data',
				'Streaming Music',
				'Multiple Lines',
				'Device Protection Plan',
				'Online Backup',
				'Avg Monthly GB Download',
				'Premium Tech Support',
				'Paperless Billing',
				'Online Security'	]
bin_list =  [	'Internet Service',
				'DSL',
				'Cable',
				'Fiber Optic',
				'Streaming TV',
				'Streaming Movies',
				'Unlimited Data',
				'Streaming Music',
				'Multiple Lines',
				'Device Protection Plan',
				'Online Backup',
				'Premium Tech Support',
				'Paperless Billing',
				'Online Security'	]
int_list = [	'Avg Monthly GB Download'	]
knn_impute(df, cor_list, 10)
binary_round(df, bin_list)
int_round(df, int_list)
for i in df.index:
	if df.at[i, 'Multiple Lines'] == 1:
		df.at[i, 'Phone Service'] = 1
	if df.at[i, 'Internet Service'] == 1:
		if df.at[i, 'Fiber Optic'] == 1:
			df.at[i, 'Cable'] = 0
			df.at[i, 'DSL'] = 0
		elif df.at[i, 'DSL'] == 1:
			df.at[i, 'Cable'] = 0
		elif not (df.at[i, 'Cable'] == 1) :
			df.at[i, 'Fiber Optic'] = 1
	else:
		df.at[i, 'Fiber Optic'] = 0
		df.at[i, 'Cable'] = 0
		df.at[i, 'DSL'] = 0

	if df.isna().at[i, 'Tenure in Months']:
		if not df.isna().at[i, 'Total Charges']:
			tmp = int(df.at[i, 'Total Charges'] / df.at[i, 'Monthly Charge'])
			tmp = 1 if tmp == 0 else tmp
			df.at[i, 'Tenure in Months'] = tmp
	if df.isna().at[i, 'Total Charges']:
		if not df.isna().at[i, 'Tenure in Months']:
			tmp = df.at[i, 'Monthly Charge'] * df.at[i, 'Tenure in Months']
			df.at[i, 'Total Charges'] = tmp


cor_list = [	'Tenure in Months',
				'Month-to-Month',
				'One Year',
				'Two Year',
				'Offer A',
				'Offer B',
				'Offer C',
				'Offer D',
				'Offer E',
				'Married'	]
bin_list = [	'Month-to-Month',
				'One Year',
				'Two Year',
				'Offer A',
				'Offer B',
				'Offer C',
				'Offer D',
				'Offer E',
				'Married'	]
int_list = [	'Tenure in Months'	]
knn_impute(df, cor_list, 10)
binary_round(df, bin_list)
int_round(df, int_list)

for i in df.index:
	if df.at[i, 'Offer B'] == 1:
		df.at[i, 'Offer A'] = 0
		df.at[i, 'Offer C'] = 0
		df.at[i, 'Offer D'] = 0
		df.at[i, 'Offer E'] = 0
	elif df.at[i, 'Offer E'] == 1:
		df.at[i, 'Offer A'] = 0
		df.at[i, 'Offer C'] = 0
		df.at[i, 'Offer D'] = 0
	elif df.at[i, 'Offer D'] == 1:
		df.at[i, 'Offer A'] = 0
		df.at[i, 'Offer C'] = 0
	elif df.at[i, 'Offer A'] == 1:
		df.at[i, 'Offer C'] = 0
	
	if df.at[i, 'Month-to-Month'] == 1:
		df.at[i, 'One Year'] = 0
		df.at[i, 'Two Year'] = 0
	elif df.at[i, 'Two Year'] == 1:
		df.at[i, 'One Year'] = 0
	elif not (df.at[i, 'One Year'] == 1):
		df.at[i, 'Month-to-Month'] = 1

	if df.isna().at[i, 'Total Charges']:
		df.at[i, 'Total Charges'] = df.at[i, 'Monthly Charge'] * df.at[i, 'Tenure in Months']


df['Phone Service'] = df['Phone Service'].fillna(df['Phone Service'].mode()).values
amldc = 'Avg Monthly Long Distance Charges'
phone_user = df.loc[df[amldc] > 0]
df[amldc] = df[amldc].fillna(phone_user[amldc].mean()).values


for i in df.index:
	if df.isna().at[i, 'Total Long Distance Charges']:
		tmp = df.at[i, 'Avg Monthly Long Distance Charges'] * df.at[i, 'Tenure in Months']
		df.at[i, 'Total Long Distance Charges'] = tmp

df['Total Refunds'] = df['Total Refunds'].fillna(0).values
df['Total Extra Data Charges'] = df['Total Extra Data Charges'].fillna(0).values


for i in df.index:
	if df.isna().at[i, 'Total Revenue']:
		tmp = 0
		tmp += df.at[i, 'Total Charges']
		tmp += df.at[i, 'Total Extra Data Charges']
		tmp += df.at[i, 'Total Long Distance Charges']
		tmp -= df.at[i, 'Total Refunds']
		df.at[i, 'Total Revenue'] = tmp




df = df.drop('Bank Withdrawal', axis=1)
df = df.drop('Credit Card', axis=1)
df = df.drop('Mailed Check', axis=1)

# Fill Satisfaction Score
scaler = MinMaxScaler()
imputer = KNNImputer(n_neighbors=15)
df = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns, index=df.index)
df = pd.DataFrame(scaler.inverse_transform(df), columns=df.columns, index=df.index)
int_round(df, ['Satisfaction Score'])

print(df)

status = pd.read_csv('status.csv').set_index('Customer ID')
df = df.join(status)

df.to_csv('merged.csv')

