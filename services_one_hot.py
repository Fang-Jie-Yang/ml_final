import pandas as pd

df = pd.read_csv('services_fixed.csv')

offer_one_hot = pd.get_dummies(df['Offer'])
df = df.drop('Offer', axis=1)
df = df.join(offer_one_hot)
df = df.drop('None', axis=1)

internet_type_one_hot = pd.get_dummies(df['Internet Type'])
df = df.drop('Internet Type', axis=1)
df = df.join(internet_type_one_hot)
df = df.drop('None', axis=1)

contract_one_hot = pd.get_dummies(df['Contract'])
df = df.drop('Contract', axis=1)
df = df.join(contract_one_hot)

payment_method_one_hot = pd.get_dummies(df['Payment Method'])
df = df.drop('Payment Method', axis=1)
df = df.join(payment_method_one_hot)

df.set_index('Customer ID').to_csv('services_fixed_one_hot.csv')
