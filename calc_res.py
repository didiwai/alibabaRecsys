import csv
#x
def userBuyItemList():
	itemlist = {}
	with open("eight.csv", "rb") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if int(row[2]) == 1:
				if row[0] in itemlist:
					if row[1] not in itemlist[row[0]]:
						itemlist[row[0]].append(row[1])
				else:
					itemlist[row[0]] = []
					itemlist[row[0]].append(row[1])
	#using eight month as predicting set 
	with open("testData.csv", "wb") as f:
		writer = csv.writer(f)
		for key in itemlist.viewkeys():
			writer.writerow([key, "|".join(itemlist[key])])


def calcResult():
	pbrandlist = []
	hitbrandlist = []
	bbrandlist = []

	pdict = createUserItemDict("itemBaseData.csv")
	tdict = createUserItemDict("testData.csv")

	realnum = 0
	for key in tdict.viewkeys():
		realnum += 1
		#Recall
		bbrandlist.append(len(tdict[key]))
		#Precision
		num = 0
		if key in pdict:
			tlist = tdict[key]
			plist = pdict[key]
			for item in tlist:
				if item in plist:
					num += 1
			hitbrandlist.append(num)
	
	for keyp in pdict.viewkeys():
		nump = len(pdict[keyp])
		pbrandlist.append(nump)
	'''
	bnum = 0
	with open("eight.csv", "rb") as f:
		reader = csv.reader(f)
		for row in reader:
			if int(row[2]) == 1:
				bnum += 1
	'''
	pre = float(sum(hitbrandlist)) / sum(pbrandlist)
	recall = float(sum(hitbrandlist)) / sum(bbrandlist)
	fscore = (2 * pre * recall) / (pre + recall)
	return [pre, recall, fscore]




def createUserItemDict(filename):
	dic = {}
	with open(filename, "rb") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			dic[row[0]] = row[1].split('|')
	return dic

if __name__ == "__main__":
	#userBuyItemList()
	res = calcResult()
	print "%f %f %f" % (res[0], res[1], res[2])
