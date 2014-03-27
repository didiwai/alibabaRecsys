import csv
import math

def ItemSimilarity(train):
	N = dict()
	C = dict()
	for u, item in train.items():
		for i in item:
			if i in N:
				N[i] += 1
			else:
				N[i] = 1
			if i not in C:
				C[i] = {} 
			for j in item:
				if i == j:
					C[i][j] = 0
					continue
				if j in C[i]:
					C[i][j] += 1
				else:
					C[i][j] = 1		
	W = dict()
	for i, related_items in C.items():
		W[i] = {}
		for j, cij in related_items.items():
			if i == j:
				W[i][j] = 0
			else:
				W[i][j] = float(cij) / math.sqrt(N[i] * N[j])

	return W


def Recommendation(ru, W, K):
	rank = dict()
	for i, pi in ru.items():
		for j, wj in sorted(W[i].items(), key=lambda x:x[1], reverse=False)[0:K]:
			if j in ru:
				continue
			if j in rank:	
				rank[j] += pi * wj
			else:
				rank[j] = pi * wj
	return rank


def processData():
	userItem = dict()
	print "process data....."
	with open("predata.csv", "rb") as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			if r[0] not in userItem:
				userItem[r[0]] = {}
			tempvalue = int(r[2])
			if tempvalue == 0:
				tempvalue = 1
			elif tempvalue == 1:
				tempvalue = 20
			elif tempvalue == 3:
				tempvalue = 10
			else:
				tempvalue = 6
			if r[1] in userItem[r[0]]:
				userItem[r[0]][r[1]] += tempvalue
			else:
				userItem[r[0]][r[1]] = tempvalue
	print "End process data...."

	print "Begin write!"
	with open("itemBaseData.csv", "wb") as csvwrite:
		writer = csv.writer(csvwrite)
		for user, itemdict in userItem.items():
			for itemid, itemvalue in itemdict.items():
				writer.writerow([user, itemid, itemvalue])
	print "End Write!"

	return userItem

def getItemUserId(name):
	userId = list()
	itemId = list()
	with open(name, "rb") as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			if r[0] not in userId:
				userId.append(r[0])
			if r[1] not in itemId:
				itemId.append(r[1])
	return userId, itemId

def getTrain(name):
	userItem = dict()
	userBuyList = dict()
	with open(name, "rb") as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			if r[0] not in userItem:
				userItem[r[0]] = {}
				userItem[r[0]][r[1]] = 1
			else:
				userItem[r[0]][r[1]] = 1

			if r[0] not in userBuyList:
				userBuyList[r[0]] = list()
				userBuyList[r[0]].append(r[1])
			elif r[1] not in userBuyList[r[0]]:
				userBuyList[r[0]].append(r[1])


	return userItem, userBuyList

if __name__ == "__main__":
	userItem = processData()
	print "get user and item id...."
	userId, itemId = getItemUserId("itemBaseData.csv")
	print "End get...."
	userItemDict, userBuyList = getTrain("itemBaseData.csv")
	W = ItemSimilarity(userItemDict)
	print "Recommend....."
	with open("ItemBaseRecommend.csv", "wb") as csvfile:
		writer = csv.writer(csvfile)
		for user in userId:
			rank = Recommendation(userItem[user], W, 10)
			t =  sorted(rank.iteritems(), key = lambda d:d[1], reverse = True)
			i = 0
			relist = []
			for item, value in t:
				if i == 5:
					break
				if item not in userBuyList[user]:
					relist.append(item)
					i += 1	
			writer.writerow([user, "|".join(relist)])

