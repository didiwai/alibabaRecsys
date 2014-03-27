import csv

dic = dict()
userlist = list()

def recPop():
	userBuyList = dict()
	with open("trainData.csv", "rb") as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if row[0] not in userlist:
				userlist.append(row[0])
			if row[0] not in userBuyList:
				userBuyList[row[0]] = list()
				userBuyList[row[0]].append(row[1])
			elif row[1] not in userBuyList[row[0]]:
				userBuyList[row[0]].append(row[1])
			if int(row[2]) == 0:
				if row[1] in dic:
					dic[row[1]] += 1
				else:
					dic[row[1]] = 1
			else:
				if row[1] in dic:
					dic[row[1]] += 1
				else:
					dic[row[1]] = 1
	return userBuyList

def recToUser(userBuyList):
	sort = sorted(dic.items(), key = lambda e:e[1], reverse = True)
	print "Create PopItem.csv file"
	with open("PopItemRecommend2.csv", "wb") as csvfile:
		writer = csv.writer(csvfile)
		for u in userlist:
			i = 0
			itemlist = []
			for item, value in sort:
				if i == 5:
					break
				#elif item not in userBuyList[u]:
				itemlist.append(item)
				i += 1
			writer.writerow([u, "|".join(itemlist)])
	print "End!"




if __name__ == "__main__":
	userBuyList = recPop()
	recToUser(userBuyList)
