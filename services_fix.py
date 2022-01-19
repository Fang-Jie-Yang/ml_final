import pandas as pd

df = pd.read_csv('services.csv')
drop_list = ['Count', 'Quarter']

# Drop Useless Columns
df = df.drop(drop_list, axis = 1)

# Yes/No => 1/0
df = df.applymap(lambda x: 1 if x == 'Yes' else (0 if x == 'No' else x))

# Internet Type => int (for simplification)
internet_type = {	'None': 0,
					'Cable': 1,
					'DSL': 2,
					'Fiber Optic': 3	}
df['Internet Type'] = df['Internet Type'].map(lambda x: internet_type[x] if x == x else x)

# Phone Service Relations
phone_acct = [	'Avg Monthly Long Distance Charges',
				'Total Long Distance Charges'	]
phone_attr = [	'Multiple Lines' ]

# Internet Service Relations
internet_acct = [	'Avg Monthly GB Download',
					'Total Extra Data Charges'	]
internet_attr = [	'Internet Type',
					'Online Security',
					'Online Backup',
					'Device Protection Plan',
					'Premium Tech Support',
					'Streaming TV',
					'Streaming Movies',
					'Streaming Music',
					'Unlimited Data'	]

# Charges Calculations
long_distance_charges = [	'Avg Monthly Long Distance Charges',
							'Tenure in Months',
							'Total Long Distance Charges'	]	
total_charges =			[	'Monthly Charge',
							'Tenure in Months',
							'Total Charges'	]
total_revenue =			[	'Total Charges',
							'Total Extra Data Charges',
							'Total Long Distance Charges',
							'Total Refunds',
							'Total Revenue'	]
# Run 3 times for (A -> B, B -> C)
for t in range(3):
	for i in range(len(df)):
		print(i)

		# Number of Referrals -> Referred a Friend
		if not df.isna().at[i, 'Number of Referrals']:
			df.at[i, 'Referred a Friend'] = int(df.at[i, 'Number of Referrals'] > 0)
		# Referred a Friend: 0 -> Number of Referrals: 0
		if not df.isna().at[i, 'Referred a Friend']:
			if df.at[i, 'Referred a Friend'] == 0:
				df.at[i, 'Number of Referrals'] = 0

		# Avg Monthly Long Distance Charges: 0 -> Phone Service: 0
		if not df.isna().at[i, 'Avg Monthly Long Distance Charges']: 
			if df.at[i, 'Avg Monthly Long Distance Charges'] == 0:
				df.at[i, 'Phone Service'] = 0
		# Total Long Distance Charges: 0 -> Phone Service: 0
		if not df.isna().at[i, 'Total Long Distance Charges']: 
			if df.at[i, 'Total Long Distance Charges'] == 0:
				df.at[i, 'Phone Service'] = 0
		# HAVE Phone Attribute -> Phone Service: 1
		for col in phone_attr:
			if not df.isna().at[i, col]: 
				if df.at[i, col] > 0:
					df.at[i, 'Phone Service'] = 1
					break
		# HAVE Phone Accounting -> Phone Service: 1
		for col in phone_acct:
			if not df.isna().at[i, col]: 
				if df.at[i, col] > 0:
					df.at[i, 'Phone Service'] = 1
					break

		# Phone Service: 0 -> Phone Accounting: 0
		# Phone Service: 0 -> Phone Attribute: 0
		if not df.isna().at[i, 'Phone Service']:
			if df.at[i, 'Phone Service'] == 0:
				for col in phone_acct:
					df.at[i, col] = 0
				for col in phone_attr:
					df.at[i, col] = 0

		# Total Long Distance Charges: 0 <-> Avg Monthly Long Distance Charges: 0
		for col in phone_acct:
			if not df.isna().at[i, col]:
				if df.at[i, col] == 0:
					for c in phone_acct:
						df.at[i, c] = 0
					break

		# Internet Type: 0 -> Internet Service: 0
		if not df.isna().at[i, 'Internet Type']: 
			if df.at[i, col] == 0:
				df.at[i, 'Internet Service'] = 0
		# Avg Monthly GB Download: 0 -> Internet Service: 0
		if not df.isna().at[i, 'Avg Monthly GB Download']: 
			if df.at[i, col] == 0:
				df.at[i, 'Internet Service'] = 0
		# HAVE Internet Attribute -> Internet Service: 1
		for col in internet_attr:
			if not df.isna().at[i, col]: 
				if df.at[i, col] > 0:
					df.at[i, 'Internet Service'] = 1
					break
		# HAVE Internet Accounting -> Internet Service: 1
		for col in internet_acct:
			if not df.isna().at[i, col]: 
				if df.at[i, col] > 0:
					df.at[i, 'Internet Service'] = 1
					break
		# Internet Service: 0 -> Internet Accounting: 0
		# Internet Service: 0 -> Internet Attribute: 0
		if not df.isna().at[i, 'Internet Service']:
			if df.at[i, 'Internet Service'] == 0:
				for col in internet_acct:
					df.at[i, col] = 0
				for col in internet_attr:
					df.at[i, col] = 0
		# Unlimited Data: 1 -> Total Extra Data Charges: 0
		if not df.isna().at[i, 'Unlimited Data']:
			if df.at[i, 'Unlimited Data'] == 1:
				df.at[i, 'Total Extra Data Charges'] = 0

		# Avg * Tenure = Total
		missing_cnt = 0
		missing = ''
		for col in long_distance_charges:
			if df.isna().at[i, col]:
				missing_cnt += 1
				missing = col
		# Can Fix If Missing Exactly One
		if missing_cnt == 1:
			avg = df.at[i, 'Avg Monthly Long Distance Charges']
			tenure = df.at[i, 'Tenure in Months']
			total = df.at[i, 'Total Long Distance Charges']
			#print("Miss:", missing)
			#print(avg, tenure, total)
			if missing == 'Avg Monthly Long Distance Charges':
				df.at[i, missing] = total / tenure
			elif missing == 'Tenure in Months':
				# Prevent row with no Phone Service
				if total != 0:
					df.at[i, missing] = int(total / avg)
			else:
				df.at[i, missing] = avg * tenure

		# Monthly * Tenure is close to Total
		missing_cnt = 0
		missing = ''
		for col in total_charges:
			if df.isna().at[i, col]:
				missing_cnt += 1
				missing = col
		# Can Fix If Missing Exactly One
		if missing_cnt == 1:
			monthly = df.at[i, 'Monthly Charge']
			tenure = df.at[i, 'Tenure in Months']
			total = df.at[i, 'Total Charges']
			if missing == 'Monthly Charge':
				df.at[i, missing] = total / tenure
			elif missing == 'Tenure in Months':
				df.at[i, missing] = int(total / monthly)
			else:
				df.at[i, missing] = monthly * tenure

		# Charges + Extra Data + Long Distance - Refunds is close to Revenue
		missing_list = []
		for col in total_revenue:
			if df.isna().at[i, col]:
				missing_list.append(col)
		# Can Fix If Missing Exactly One
		if len(missing_list) == 1:
			missing = missing_list[0]
			charges = df.at[i, 'Total Charges']
			extra = df.at[i, 'Total Extra Data Charges']
			long_dist = df.at[i, 'Total Long Distance Charges']
			refund = df.at[i, 'Total Refunds']
			revenue = df.at[i, 'Total Revenue']
			if missing == 'Total Charges':
				val = (revenue + refund - long_dist - extra)
				df.at[i, missing] = val if val >= 0.1 else 0
			if missing == 'Total Extra Data Charges':
				val = (revenue + refund - long_dist - charges)
				df.at[i, missing] = val if val >= 0.1 else 0
			if missing == 'Total Long Distance Charges':
				val = (revenue + refund - extra - charges)
				df.at[i, missing] = val if val >= 0.1 else 0
			if missing == 'Total Refunds':
				val = (charges + extra + long_dist - revenue)
				df.at[i, missing] = val if val >= 0.1 else 0
			if missing == 'Total Revenue':
				val = (charges + extra + long_dist - refund)
				df.at[i, missing] = val if val >= 0.1 else 0

reverse_internet_type = {	0: 'None',
							1: 'Cable',
							2: 'DSL',
							3: 'Fiber Optic'	}
df['Internet Type'] = df['Internet Type'].map(lambda x: reverse_internet_type[x] if x == x else x)
df.set_index('Customer ID').to_csv('services_fixed.csv')
