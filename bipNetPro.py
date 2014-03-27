import csv


def processData():
	userItem = dict()
	print "process data....."
	with open("oneToSeven.csv", "rb") as csvfile:
		reader = csv.reader(csvfile)
		for r in reader:
			if r[0] not in userItem:
				userItem[r[0]] = {}
			tempvalue = int(r[2])
			if tempvalue == 2:
				tempvalue = 0
			elif tempvalue == 3:
				tempvalue = 0
			if r[1] in userItem[r[0]]:
				userItem[r[0]][r[1]] += tempvalue
			else:
				userItem[r[0]][r[1]] = tempvalue
	print "End process data...."
	print "Begin write!"
	with open("bipNetProData.csv", "wb") as csvwrite:
		writer = csv.writer(csvwrite)
		for user, itemdict in userItem.items():
			for itemid, itemvalue in itemdict.items():
				writer.writerow([user, itemid, itemvalue])
	print "End Write!"

def CreateWright(degreex, degreey, edgeweight, wij, user):
	W = dict()
	n = len(wij)
	with open("MatrixWeight.csv", "wb") as csvfile:
		writer = csv.writer(csvfile)
		temp = 1
		for i in wij:
			print "ALL:	" + str(n) + "NO:    " + str(temp)
			if i not in W:
				W[i] = dict()
			for j in wij:
				t_value = 0
				for l in user:
					try:
						if degreey[l] != 0:
							if (edgeweight[i][l] != 0) and (edgeweight[j][l] != 0):
								t_value += float(edgeweight[i][l] * edgeweight[j][l]) / degreey[l]
							else:
								t_value += 0
					except:
						pass
				if degreex[j] == 0:
					W[i][j] = 0
				else:
					W[i][j] = t_value / degreex[j]
				writer.writerow([i, j, W[i][j]])
			temp += 1
	return W

def BipNetwork():
	degreex = dict()	#item
	degreey = dict()	#user
	edgeweight = dict() #a
	wij = list()		#item
	user = list()	#m
	initalsource = dict()#f
	print "create inital data......."
	with open("bipNetProData.csv", "rb") as readfile:
		reader = csv.reader(readfile)
		for r in reader:
			t_value = int(r[2])

			if r[1] not in wij :
				wij.append(r[1])
			if r[0] not in user:
				user.append(r[0])

			if r[1] not in edgeweight:
				edgeweight[r[1]] = dict()
				edgeweight[r[1]][r[0]] = t_value
			else:
				edgeweight[r[1]][r[0]] = t_value

			if r[0] not in degreey:
				degreey[r[0]] = t_value
			else:
				degreey[r[0]] += t_value

			if r[1] not in degreex:
				degreex[r[1]] = t_value
			else:
				degreex[r[1]] += t_value

			if r[1] not in initalsource:
				initalsource[r[1]] = t_value
			else:
				initalsource[r[1]] += t_value
	print "End create intial data......"
	userNum = len(user)
	itemNum = len(wij)
	recommendItemList = dict()#f(x)
	print "Create Wright Matrix W........"
	
	W = CreateWright(degreex, degreey, edgeweight, wij, user)
	'''
	W = dict()
	with open("MatrixWeight.csv", "rb") as matrixfile:
		reader = csv.reader(matrixfile)
		tem_num = 1
		for r in reader:
			if tem_num % 1000000 == 0:
				print "NO: " + str(tem_num)
			if r[0] not in W:
				W[r[0]] = dict()
				W[r[0]][r[1]] = float(r[2])
			else:
				W[r[0]][r[1]] = float(r[2])	
			tem_num += 1
	'''
	print "End......"
	print "Create Recommend Item List....."
	t_num = 0
	for i in wij:
		if t_num % 1000 == 0:
			print "Recommend Item List NO:	" + str(t_num)
		tempvalue = 0
		for j in wij:
			tempvalue += W[i][j] * initalsource[j]
		recommendItemList[i] = tempvalue
		t_num += 1
	print "End......"
	t =  sorted(recommendItemList.iteritems(), key = lambda d:d[1], reverse = True)
	print "write the result into file......"
	with open("bipNetProRecommend.csv", "wb") as writefile:
		writer = csv.writer(writefile)	
		for u in user:
			relist = list()
			num = 0
			for item, value in t:
				if num == 5:
					break
				elif item in edgeweight:
					if (u in edgeweight[item]) and (edgeweight[item][u] == 0):
						relist.append(item)
						num += 1
					elif u not in edgeweight[item]:
						relist.append(item)
						num += 1
				else:
					relist.append(item)
					num += 1 
			writer.writerow([u, "|".join(relist)])
	print "End write......."




if __name__ == "__main__":
	#processData()
	BipNetwork()