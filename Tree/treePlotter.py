import matplotlib.pyplot as plt

#定义文本框和箭头格式
decisionNode = dict(boxstyle = "sawtooth", fc = "0.8")
leafNode = dict(boxstyle = "round4", fc = "0.8")
arrow_args = dict(arrowstyle = "<-")

#绘制带箭头的注释
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
	#xy为被注释的点，xytext为注释文字的坐标位置
	createPlot.ax1.annotate(nodeTxt, xy = parentPt, \
		xycoords = 'axes fraction', xytext = centerPt, \
		textcoords = 'axes fraction', va = 'center', ha = 'center', \
		bbox = nodeType, arrowprops = arrow_args)

#def createPlot():
#	fig = plt.figure(1, facecolor = 'white')
#	fig.clf()
#	createPlot.ax1 = plt.subplot(111, frameon = False)
	#createPlot.ax1为全局变量
#	plotNode('Decision Node', (0.5, 0.1), (0.1, 0.5), decisionNode)
#	plotNode('LeafNode', (0.8, 0.1), (0.1, 0.8), leafNode)
#	plt.show()

''' 绘制一颗完整的树需要确定叶节点以便可以正确确定x轴的长度
	需要知道树有多少层，以便可以正确确定y轴的高度 '''
def getNumLeafs(myTree):
	numLeafs = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			numLeafs += getNumLeafs(secondDict[key])
		else:
			numLeafs += 1
	return numLeafs
	
def getTreeDepth(myTree):
	maxDepth = 0
	firstStr = list(myTree.keys())[0]
	secondDict = myTree[firstStr]
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			thisDepth = 1 + getTreeDepth(secondDict[key])
		else:
			thisDepth = 1
		if thisDepth > maxDepth:
			maxDepth = thisDepth
	return maxDepth
	
def plotMidText(cntrPt, parentPt, txtString):
	xMid = (parentPt[0] - cntrPt[0]) / 2 + cntrPt[0]
	yMid = (parentPt[1] - cntrPt[1]) / 2 + cntrPt[1]
	createPlot.ax1.text(xMid, yMid, txtString)
	
def plotTree(myTree, parentPt, nodeTxt):
	numLeafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)
	firstStr = list(myTree.keys())[0]
	cntrPt = (plotTree.xOff + (1 + float(numLeafs)) / 2.0 / plotTree.totalW, \
		plotTree.yOff)
	plotMidText(cntrPt, parentPt, nodeTxt)
	plotNode(firstStr, cntrPt, parentPt, decisionNode)
	secondDict = myTree[firstStr]
	plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
	for key in secondDict.keys():
		if type(secondDict[key]).__name__ == 'dict':
			plotTree(secondDict[key], cntrPt, str(key))
		else:
			plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
			plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), \
				cntrPt, leafNode)
			plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
	plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD

def createPlot(inTree):
	fig = plt.figure(1, facecolor = 'white')
	fig.clf()
	axprops = dict(xticks = [], yticks = [])
	createPlot.ax1 = plt.subplot(111, frameon = False, **axprops)
	plotTree.totalW = float(getNumLeafs(inTree))
	plotTree.totalD = float(getTreeDepth(inTree))
	plotTree.xOff = -0.5 / plotTree.totalW
	plotTree.yOff = 1.0
	plotTree(inTree, (0.5, 1.0), '')
	plt.show()
	
def retrieveTree(i):
	listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':{0:'no', 1:'yes'}}}}, \
				{'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no', 1:'yes'}}, 1:'no'}}}}]
	return listOfTrees[i]
	


