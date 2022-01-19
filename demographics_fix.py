import pandas as pd

df = pd.read_csv('demographics.csv')
drop_list = ['Count']

# Drop Useless Columns
df = df.drop(drop_list, axis = 1)

# Yes/No => 1/0
df = df.applymap(lambda x: 1 if x == 'Yes' else (0 if x == 'No' else x))
# Male/Female => 1/0
df = df.applymap(lambda x: 1 if x == 'Male' else (0 if x == 'Female' else x))

for i in range(len(df)):

	# Age -> Under 30, Senior Citizen
	if not df.isna().at[i, 'Age']:
		df.at[i, 'Under 30'] = int(df.at[i, 'Age'] < 30)
		df.at[i, 'Senior Citizen'] = int(df.at[i, 'Age'] >= 65)

	# Under 30 -> NOT Senior Citizen
	if not df.isna().at[i, 'Under 30']:
		if df.at[i, 'Under 30'] == 1:
			df.at[i, 'Senior Citizen'] = 0
	# Senior Citizen -> NOT Under 30
	if not df.isna().at[i, 'Senior Citizen']:
		if df.at[i, 'Senior Citizen'] == 1:
			df.at[i, 'Under 30'] = 0

	# Number of Dependents -> Dependents
	if not df.isna().at[i, 'Number of Dependents']:
		df.at[i, 'Dependents'] = int(df.at[i, 'Number of Dependents'] > 0)

	# Dependents: 0 -> Number of Dependents: 0
	if not df.isna().at[i, 'Dependents']:
		if df.at[i, 'Dependents'] == 0:
			df.at[i, 'Number of Dependents'] = 0

df.set_index('Customer ID').to_csv('demographics_fixed.csv')
