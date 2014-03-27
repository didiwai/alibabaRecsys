import csv

def union(nameone, nametwo, writename):
	dictone = dict()
	dicttwo = dict()
	dictresult = dict()
	print "read csvfile one....."
	with open(nameone, "rb") as rone:
		readone = csv.reader(rone)
		for rowone in readone:
			dictone[rowone[0]] = list()
			if rowone[1] != "":
				dictone[rowone[0]] = rowone[1].split('|')
	print "read csvfile two....."
	with open(nametwo, "rb") as rtwo:
		readtwo = csv.reader(rtwo)
		for rowtwo in readtwo:
			dicttwo[rowtwo[0]] = list()
			if rowtwo[1] != "":
				dicttwo[rowtwo[0]] = rowtwo[1].split('|')
	print "Create result file list...."
	for u, l in dictone.items():
		dictresult[u] = list()
		if len(l) == 0:
			dictresult[u] = dicttwo[u]
		else:
			dictresult[u] = l
			if len(dicttwo[u]) != 0:
				for i in dicttwo[u]:
					if i not in dictresult[u]:
						dictresult[u].append(i)
		'''
		if len(dictresult[u]) > 5:
			dictresult[u] = dictresult[u][0:5]
		'''
	print "Create result file........."
	with open(writename, "wb") as writefile:
		writer = csv.writer(writefile)
		for user, relist in dictresult.items():
			writer.writerow([user, '|'.join(relist)])
if __name__ == "__main__":
	union("ItemIntersectUserRecommend.csv", "PopItemRecommend.csv", "UserItemUnionPop.csv")