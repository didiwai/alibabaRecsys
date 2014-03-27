import csv


def intersect(objectOne, objectTwo, writename):
	dictone = dict()
	dicttwo = dict()
	dictresult = dict()
	print "read csvfile one....."
	with open(objectOne, "rb") as rone:
		readone = csv.reader(rone)
		for rowone in readone:
			dictone[rowone[0]] = list()
			dictone[rowone[0]] = rowone[1].split('|')
	print "read csvfile two....."
	with open(objectTwo, "rb") as rtwo:
		readtwo = csv.reader(rtwo)
		for rowtwo in readtwo:
			dicttwo[rowtwo[0]] = list()
			dicttwo[rowtwo[0]] = rowtwo[1].split('|')
	print "Create result file list...."
	for u, l in dictone.items():
		dictresult[u] = list()
		for reitem in l:
			if reitem in dicttwo[u]:
				dictresult[u].append(reitem)
	print "Create result file........."
	with open(writename, "wb") as writefile:
		writer = csv.writer(writefile)
		for user, relist in dictresult.items():
			writer.writerow([user, '|'.join(relist)])

if __name__ == "__main__":
	intersect("ItemIntersectUserRecommend.csv", "PopItemRecommend.csv", "UserItemIntersectPopRecommend.csv")
