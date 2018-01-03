import time, os
import csv, codecs
import pandas as pd
import numpy as np
# csvfile = codecs.open('PPPProjects_Info.csv', 'r', 'utf-8')
df = pd.read_csv('PPPProjects_Info.csv')
# print (df['投资金额'].values.tolist())
# print (type(csvfile))

ninvest = []
for item in df['投资金额'].values.tolist():
	ninvest.append(item.replace(",", '').strip())
# print (ninvest)
df['投资金额'] = ninvest
nprovince = []
ncity = []
ndistrict = []
for item in df['地点'].values.tolist():
	tokens = item.split(' > ')
	if len(tokens) < 3:
		for i in range(3-len(tokens)):
			tokens.append('')
	nprovince.append(tokens[0])
	ncity.append(tokens[1])
	ndistrict.append(tokens[2])
df.drop('地点', axis=1, inplace=True)
df.insert(1, '省', nprovince)
df.insert(2, '市', ncity)
df.insert(3, '区', ndistrict)
df.to_csv('PPPProjects_Info_20180103.csv', index=False, header=True)