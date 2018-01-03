import time, os
import csv, codecs
csvfile = codecs.open('PPPProjects_Info.csv', 'r', 'utf-8')
newfile = codecs.open('PPPProjects_Info_20180103.csv', 'w', 'utf_8_sig')
flag = False
content = []
writer = csv.writer(newfile)
writer.writerow(['项目名称', '省', '市', '区','发起时间', '投资金额', '发起人', '类型', 'RID'])
count = 1
for line in csvfile:
	if not flag:
		flag = True
		continue
	line = line[:-1]
	tokens = line.split(',')
	if len(tokens) == 1:
		a = csvfile.readline()
		line = line + a
		tokens = line.split(',')
	try:
		locations = tokens[1].split(' > ')
		# a = csvfile.readline()
		# line = line + a
	except:
		print (count, line)
		exit()
	if len(locations) < 3:
		for i in range(3 - len(locations)):
			locations.append('')
	newline = [tokens[0]] + locations + tokens[2:-1] + [tokens[-1].strip()]
	writer.writerow(newline)
	count += 1
csvfile.close()