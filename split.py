import pandas as pd

train = pd.read_csv('Train_IDs.csv').set_index('Customer ID')
test = pd.read_csv('Test_IDs.csv').set_index('Customer ID')

df = pd.read_csv('merged.csv').set_index('Customer ID')

print(len(train))
train = train.join(df).dropna(how='all')
print(len(train))
train = train.dropna()
print(len(train))
test = test.join(df)

train.to_csv('train.csv')
test.to_csv('test.csv')



