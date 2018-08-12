from numpy import *
import operator
import matplotlib.pyplot as plt
import os

def creatDataSet():
	group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
	labels = ['A', 'A', 'B', 'B']
	return group, labels

''' kNN algorithm '''	
def classify0(inx, dataSet, labels, k):
	dataSetSize = dataSet.shape[0]		#取其row
	diffMat = tile(inx, (dataSetSize, 1)) - dataSet		#tile(a,(x,y))将a按(x,y)行列表示
	sqDiffMat = diffMat ** 2
	sqDistance = sqDiffMat.sum(axis = 1)			#equal to matlab sum(A, 2)
	Distance = sqDistance ** 0.5
	sortedDistIndicies = Distance.argsort()			#升序排列，索引表示
	classCount = {}
	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		#dict.get()方法，没找到就返回第二个参数的值
		classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
		sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), \
			reverse = True)		#itemgetter(1)表示按照第二个元素次序对元组排序
	return sortedClassCount[0][0]
	
''' kNN改进约会网站的配对 '''
def file2matrix(filename):
	fr = open(filename)
	arrayOLines = fr.readlines()
	numberOfLines = len(arrayOLines)
	returnMat = zeros((numberOfLines, 3))		
	classLabelVector = []
	index = 0
	for line in arrayOLines:
		line = line.strip()		#去掉换行
		listFromLine = line.split('\t')
		returnMat[index, :] = listFromLine[0:3]
		classLabelVector.append(int(listFromLine[-1]))
		index += 1
	return returnMat, classLabelVector
	
def autoNorm(dataSet):
	''' 归一化 '''
	minVals = dataSet.min(0)		#返回每列最小值
	maxVals = dataSet.max(0)
	ranges = maxVals - minVals
	#shape(A) return (A rows x A columns)
	normDataSet = zeros(shape(dataSet))
	m = dataSet.shape[0]
	normDataSet = dataSet - tile(minVals, (m, 1))
	normDataSet = normDataSet / tile(ranges, (m, 1))
	return normDataSet, ranges, minVals
	
def datingClassTest():
	hoRatio = 0.10		#use %10 examples for test
	datingMat, datingLabels = file2matrix('datingTestSet2.txt')
	normMat, ranges, minVals = autoNorm(datingMat)
	m = normMat.shape[0]
	numTesrVecs = int(m * hoRatio)		#int for for loop
	errorCount = 0.0
	for i in range(numTesrVecs):
		classifierResult = classify0(normMat[i, :], normMat[numTesrVecs:m, :], \
			datingLabels[numTesrVecs:m], 4)		#datingLabels is a list
		print("the classfier came back with: %d, the real answer is: %d" \
			% (classifierResult, datingLabels[i]))
		if classifierResult != datingLabels[i]:
			errorCount += 1
	print("The accuracy is: %f" % (1.0 - (errorCount / float(numTesrVecs))))

def classifyPerson():
	''' dating predict '''
	resultList = ['not at all', 'in small doses', 'in large doses']
	percentTats = float(input("percentage of spent playing video games? "))
	ffMiles = float(input("frequent flier miles earned per year? "))
	iceCream = float(input("liters of ice cream consumed per year? "))
	datingMat, datingLabels = file2matrix('datingTestSet2.txt')
	normMat, ranges, minVals = autoNorm(datingMat)
	inArr = array([ffMiles, percentTats, iceCream])
	classifierResult = classify0((inArr - minVals) / ranges, normMat, datingLabels, 3)
	print("You will probably like this person: ", \
		resultList[classifierResult - 1])

		
''' kNN识别手写数字 '''	
def img2vector(filename):
	''' 将32x32的二进制图像转换为1x1024的向量 '''
	''' 循环读出32行，并循环将每行32个数值存储在Numpy数组中 '''
	returnVect = zeros((1, 1024))
	fr = open(filename)
	for i in range(32):
		lineStr = fr.readline()
		for j in range(32):
			returnVect[0, 32 * i + j] = int(lineStr[j])
	return returnVect
	
def handwritingClassTest():
	hwLabels = []
	trainingFileList = os.listdir('trainingDigits')
	m = len(trainingFileList)
	trainingMat = zeros((m, 1024))
	for i in range(m):
		fileNameStr = trainingFileList[i]
		fileStr = fileNameStr.split('.')[0]
		classNumber = int(fileStr.split('_')[0])
		hwLabels.append(classNumber)
		trainingMat[i, :] = img2vector("trainingDigits/%s" % fileNameStr)
	testFileList = os.listdir('testDigits')
	mTest = len(testFileList)
	#记录错误次数和错误的文件位置
	error_Count = 0.0
	error_Indices = []
	for j in range(mTest):
		fileNameStr = testFileList[j]
		fileStr = fileNameStr.split('.')[0]
		classNumber = int(fileStr.split('_')[0])
		vectorUnderTest = img2vector("testDigits/%s" % fileNameStr)
		classifierResult = classify0(vectorUnderTest, trainingMat, \
			hwLabels, 3)
		print("the classifier came back with : %d, the real result is : %d" \
			 % (classifierResult, classNumber))
		if classifierResult != classNumber:
			error_Count += 1.0
			error_Indices.append(fileNameStr)
	print("\nthe wrong predictions happen in : %s" % error_Indices)
	print("\nthe total number of errors is : %d" % error_Count)
	print("\nthe total error rate is : %f" % (error_Count / float(mTest)))
	
#可以看出kNN算法的效率并不高，算法需要为每个测试向量做2000次的距离计算，而向量涉及1024维
#的浮点数运算，且总计进行900次，此外测试向量内存占用也不小
#k决策树就是k近邻算法的优化版，可以节省大量的计算开销
	
'''
fig = plt.figure()
plt.xlabel("video games occupied ratio")
plt.ylabel("liters of icecream on weekly purchase")
ax = fig.add_subplot(111)
ax.scatter(datingMat[:, 1], datingMat[:, 2], 15.0 * array(datingLabels), \
	15.0 * array(datingLabels))
plt.show()
'''