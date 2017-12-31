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
import requests
url = "http://www.cpppc.org:8082/efmisweb/ppp/projectLibrary/getPPPList.do"
headers = {"Connection": "keep-alive",
			"Host": "www.cpppc.org:8082",
			"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
			'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
			'cookie': 'faspjsessionid=-6OsIB9ByX_ZXsBnKCwcPyKAJY8vBxkMisTsuHcItDBfNQcFK2yQ!1795877700; JSESSIONID=O22sdDF2E8cTwwH2G5lYLcv2CAoor7SUf9bs4sN35oWrFon34rhr!879924186'}
MAX_PAGE = 1758

res = []

async def getPage(session, n):
	# print (n)
	postdata = {'queryPage': 1300,
				'distStr': 'all'}
	async with session.post(url, data=json.dumps(postdata), headers=headers) as r:
		# print (await json.loads(r.text())['currentPage'])
		# print (n)
		# print (await r.json())
		a = await r.text()
		print (a)
		return a
		# return await r.json()
		# return await r.text()

def crawlerSync():
	start = time.time()
	for i in range(1, MAX_PAGE+1):
		r = requests.post(url, headers=headers, data = {'queryPage': i})
		# print (r.json())
		res.append(r.json())
		print ('Finished: {}/{}'.format(i, MAX_PAGE))
	t = time.time() - start 
	print ("Consumed: {:.4f}s".format(t))


def crawler():
	start = time.time()
	for i in range(MAX_PAGE // 100 + 1):
		st = i*100+1
		ed = min(st+99, MAX_PAGE)
		loop = asyncio.get_event_loop()
		tasks = []
		with aiohttp.ClientSession(loop=loop) as session:
			for j in range(st, ed+1):
				tasks.append(asyncio.ensure_future(getPage(session, j)))
			loop.run_until_complete(asyncio.gather(*tasks))
			for task in tasks:
				res.append(task.result())
				# print (res)
			print ('Finished: {}/{}'.format(ed, MAX_PAGE))
	t = time.time() - start 
	print ("Consumed: {:.4f}s".format(t))

def dumpcsv():
	csvfile = codecs.open('PPPProjects_Info.csv', 'w', 'utf_8_sig')
	writer = csv.writer(csvfile)
	writer.writerow(['项目名称', '地点', '发起时间', '投资金额', '发起人', '类型', 'RID'])
	for r in res:
		for item in r['list']:
			# print (item)
			writer.writerow([item['PROJ_NAME'],
							 item['PRV'],
							 item['START_TIME'],
							 item['INVESTCOUNT'],
							 item['START_UNAME'],
							 item['IVALUE'],
							 item['PROJ_RID']
							 ])

	csvfile.close()

# crawler()
crawlerSync()
dumpcsv()