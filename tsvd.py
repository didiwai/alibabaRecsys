# -*- coding: utf-8 -* 
from numpy import *
from numpy import linalg as la

# 载入数据 (用户-菜肴矩阵)
# 行为 用户, 列为希肴, 表示用户对某个菜肴的评分
def loadExData2():
	return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
			 [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
			 [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
			 [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
			 [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
			 [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
			 [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
			 [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
			 [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
			 [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
			 [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]
	
# 计算两个评分的 欧氏距离
def ecludSim(inA,inB):
	return 1.0/(1.0 + la.norm(inA - inB))

# 计算两个评分的 皮尔逊相关系数 (Pearson Correlation)
def pearsSim(inA,inB):
	if len(inA) < 3 : return 1.0
	return 0.5+0.5*corrcoef(inA, inB, rowvar = 0)[0][1]

# 计算两个评分的 余弦相似度 (Cosine similarity)
def cosSim(inA,inB):
	num = float(inA.T*inB)
	denom = la.norm(inA)*la.norm(inB)
	return 0.5+0.5*(num/denom)


# 基于物品相似度, 计算用户对物体的评分估计值
# 参数 simMeas 为 相似度计算方法
# 参数 user 为用户编号
# 参数 item 为物品编号
def standEst(dataMat, user, simMeas, item):
	n = shape(dataMat)[1] # 矩阵列数, 即物品数
	simTotal = 0.0; 
	ratSimTotal = 0.0

	# 遍历每个物品 
	for j in range(n):
		userRating = dataMat[user,j]	# 用户对 j 物品的评分, 取不为 0 的计算相似度
		if userRating == 0: continue
		
		# overLap 为某个用户都评分的两个物品
		# 即某个用户在评分了物品 item 后, 还评分了物品 j, 返回找到的第一个用户 
		# 把第 item 列与 j 列求 与, 并取第一个不为 0 的行作为 overLap
		overLap = nonzero(logical_and(dataMat[:,item].A>0, dataMat[:,j].A>0))[0]
		 
		if len(overLap) == 0: similarity = 0
		else: 
			# 计算两个物品评分的相似度
			similarity = simMeas(dataMat[overLap,item], dataMat[overLap,j])

		simTotal += similarity
		ratSimTotal += similarity * userRating

	if simTotal == 0: return 0
	else: return ratSimTotal/simTotal	 # 归一化


# 基于 SVD,	计算用户对物体的评分估计值
def svdEst(dataMat, user, simMeas, item):
	n = shape(dataMat)[1]
	simTotal = 0.0; 
	ratSimTotal = 0.0

	for j in range(n):
		userRating = dataMat[user,j]	# 用户对 j 物品的评分, 取不为 0 的计算相似度
		if userRating == 0 or j==item: continue
		# 计算两个物品评分的相似度
		similarity = simMeas(xformedItems[item,:].T, xformedItems[j,:].T)

		simTotal += similarity
		ratSimTotal += similarity * userRating

	if simTotal == 0: return 0
	else: return ratSimTotal/simTotal


# 推荐引擎 
# 即寻找用户未评分的物品, 并基于物品相似度进行评分
# 对用户评过分的物品, 自然是以他自己的评分为主 
# 参数 N 为按推荐分数从高到低返回前 N 个推荐的物品
def recommend(dataMat, user, N = 5, simMeas = cosSim, estMethod = svdEst):
	# 寻找用户未评分的物品
	unratedItems = nonzero(dataMat[user,:].A==0)[1] 
	if len(unratedItems) == 0: return 'you rated everything'

	itemScores = []
	for item in unratedItems:
		# 获取用户对物品 item 的评分的估计值
		estimatedScore = estMethod(dataMat, user, simMeas, item)
		itemScores.append((item, estimatedScore))
	# 按推荐分数从高到低返回前 N 个推荐的物品
	return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]


if __name__ == "__main__":
	myMat = mat(loadExData2())
	U,Sigma,VT = la.svd(myMat)					# SVD 分解
	# 构建对角距阵, 这里只取前 5 个奇异值, 5 是额外计算出来的, 确保包含能量高于总能量 90%
	Sig4 = mat(eye(5)*Sigma[:5])	
	xformedItems = dataMat.T * U[:,:5] * Sig4.I	 # 将高维转为低维, 构建转换后的物品
	print recommend(myMat, 1)
  '''
	num = 1
	temp = Sigma[0]
	sumvalue = sum(Sigma)
	while temp <= sumvalue * 0.9:
		temp += Sigma[num]
		num += 1
	print num
  '''
#	print recommend(myMat, 1, estMethod=standEst)
#	print recommend(myMat, 1, estMethod=svdEst)