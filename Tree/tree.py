from math import log
import operator

#计算信息增益
def calcShannonEnt(dataSet):
	numEntries = len(dataSet)
	labelCount = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if not currentLabel in labelCount.keys():
			labelCount[currentLabel] = 0
		labelCount[currentLabel] += 1
	shannonEnt = 0.0
	for key in labelCount:				#所有分类
		prob = float(labelCount[key] / numEntries)
		shannonEnt -= prob * log(prob, 2)		#信息增益公式
	return shannonEnt
	
def createDataSet():
	dataSet = [[1, 1, 'yes'], \
			   [1, 1, 'yes'], \
			   [1, 0, 'no'], \
			   [0, 1, 'no'], \
			   [0, 1, 'no']]
	labels = ['no surfacing', 'flippers']
	return dataSet, labels
	
def splitDataSet(dataSet, axis, value):
	#axis为划分数据集的特征
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis + 1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet

#选择最好的数据集划分方式
def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0]) - 1
	baseEntropy = calcShannonEnt(dataSet)
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeatures):
		#create a list of all the examples of this feature
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)		#将某个类的取值集合
		newEntropy = 0.0
		#遍历当前特征所有唯一属性值，对每个唯一属性值划分一次数据集
		#然后进行熵值求和
		#信息增益是熵的减少或信息无序度的减少
		for value in uniqueVals:
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet) / float(len(dataSet))
			#计算新熵值
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		if infoGain > bestInfoGain:
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature	

def majorityCnt(classList):
	#处理了所有属性，但类标签还不是唯一，采用多数表决的方式
	#又利用了字典的operator.itemgetter(1)操作key排序
	classCount = {}
	for vote in classList:
		if not vote in classCount.keys():
			classCount[vote] = 0
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.items(), \
		key = operator.itemgetter(1), reverse = True)
	return sortedClassCount[0][0]
	
def createTree(dataSet, labels):
	''' 递归生成树 '''
	classList = [example[-1] for example in dataSet]
	#类别完全相同，停止划分
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	#遍历完所有特征时返回出现次数最多的类别
	if len(dataSet[0]) == 1:
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	myTree = {bestFeatLabel:{}}			#递归的嵌套字典
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		#python语言中函数类型是List时，参数是按照引用方式传递的
		#为了不改变原始List的内容，使用新变量subLabels代替
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet \
			(dataSet, bestFeat, value), subLabels)
	return myTree
	
def classify(inputTree, featLabels, testVec):
	firstStr = list(inputTree.keys())[0]		#python3不支持字典keys()索引
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)		#index方法找到第一个匹配的索引值
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classify(secondDict[key], featLabels, testVec)
			else:
				classLabel = secondDict[key]
	return classLabel
	
''' 构造决策树是很耗时的任务，使用python的pickle模块序列化对象，
	可以进行决策树在磁盘上的存储 '''
def storeTree(inputTree, filename):
	import pickle
	with open(filename, 'wb+') as f_obj:
		pickle.dump(inputTree, f_obj)
	#fw = open(filename, 'wb+')			#pickle存储默认为二进制
	#pickle.dump(inputTree, fw)
	#fw.close()
	
def grabTree(filename):
	import pickle
	fr = open(filename, 'rb+')
	return pickle.load(fr)