import time, os
import csv, codecs
# import pandas as pd

# json file:
# totalCount:
# list: [{
# 	PROJ_NAME 名称
# 	PRV 地点 (* > * > *)
# 	START_TIME 发起时间 （yyyy-mm-dd）
# 	INVESTCOUNT 投资金额 （单位：万元）
# 	START_UNAME 发起人？
# 	IVALUE  类型？
#   PROJ_RID 
# }]

# POST
# queryPage: int


import asyncio
import aiohttp
import json

url = "http://www.cpppc.org:8082/efmisweb/ppp/projectLibrary/getPPPList.do"

MAX_PAGE = 1758

res = []

async def getPage(n):
	postdata = {'queryPage': n}
	async with aiohttp.ClientSession() as session:
		async with session.post(url, json=postdata) as r:
			# print (json.loads(r.read())['currentPage'])
			# print (n)
			return await r.text()


def crawler():
	start = time.time()
	for i in range(MAX_PAGE // 100 + 1):
		st = i*100+1
		ed = min(st+99, MAX_PAGE)
		tasks = [asyncio.ensure_future(getPage(j)) for j in range(st, ed+1)]
		loop = asyncio.get_event_loop()
		loop.run_until_complete(asyncio.wait(tasks))
		for task in tasks:
			res.append(task.result())
		print ('Finished: {}/{}'.format(ed, MAX_PAGE))
	t = time.time() - start 
	print ("Consumed: {:.4f}s".format(t))

def dumpcsv():
	csvfile = codecs.open('PPPProjects_Info.csv', 'w', 'utf_8_sig')
	writer = csv.writer(csvfile)
	writer.writerow(['项目名称', '地点', '发起时间', '投资金额', '发起人', '类型', 'RID'])
	for r in res:
		jobj = json.loads(r)
		for item in jobj['list']:
			writer.writerow([item['PROJ_NAME'],
							 item['PRV'],
							 item['START_TIME'],
							 item['INVESTCOUNT'],
							 item['START_UNAME'],
							 item['IVALUE'],
							 item['PROJ_RID']
							 ])

	csvfile.close()

crawler()
dumpcsv()