import csv
import math


def UserSimilarity(train): 
	# build inverse table for item_users 
	item_users = dict() 
	for u, items in train.items(): 
		for i in items.keys(): 
			if i not in item_users: 
				item_users[i] = set() 
			item_users[i].add(u) 
	#calculate co-rated items between users 
	C = dict() 
	N = dict() 
	for i, users in item_users.items(): 
		for u in users: 
			if u in N:
				N[u] += 1
			else:
				N[u] = 1
			if u not in C:
				C[u] = {} 
			for v in users: 
				if u == v: 
					continue 
				if v in C[u]:
					C[u][v] += 1 
				else:
					C[u][v] = 1
	#calculate finial similarity matrix W 
	W = dict() 
	for u, related_users in C.items(): 
		W[u] = {}
		for v, cuv in related_users.items(): 
			W[u][v] = float(cuv) / math.sqrt(N[u] * N[v]) 
	return W


def Recommend(user, train, W, K):
	rank = dict()
	interacted_items = train[user]
	for v, wuv in sorted(W[user].items(), key=lambda x:x[1], reverse = True)[0:K]:
		for i, rvi in train[v].items():
			if i in interacted_items:
				#we should filter items user interacted before
				continue
			if i in rank:
				rank[i] += wuv * rvi 
			else:
				rank[i] = wuv * rvi
	return rank


def processData():
	userItem = dict()
	print "process data....."
	with open("trainData.csv", "rb") as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			if r[0] not in userItem:
				userItem[r[0]] = {}

			tempvalue = int(r[2])
			userItem[r[0]][r[1]] = tempvalue

	print "End process data...."
	print "Begin write!"
	with open("userBaseData.csv", "wb") as csvwrite:
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
	with open(name, "rb") as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			if r[0] not in userItem:
				userItem[r[0]] = {}
			userItem[r[0]][r[1]] = 1
	return userItem

if __name__ == "__main__":
	userItem = processData()
	print "get user and item id...."
	userId, itemId = getItemUserId("userBaseData.csv")
	print "End get...."
	userItemDict = getTrain("userBaseData.csv")
	W = UserSimilarity(userItemDict)
	print "Recommend....."
	with open("UserBaseRecommend.csv", "wb") as csvfile:
		writer = csv.writer(csvfile)
		for user in userId:
			rank = Recommend(user, userItemDict, W, 10)
			t =  sorted(rank.iteritems(), key = lambda d:d[1], reverse = True)
			i = 0
			relist = []
			for item, value in t:
				if i == 5:
					break
				relist.append((item, value))
				i += 1
			#writer.writerow([user, "|".join(relist)])
			writer.writerow([user, relist])
