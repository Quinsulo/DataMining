# 决策属性：是否适合运动
# 条件属性：天气outlook，温度temperature，湿度humidity，风况windy
# 一列数据对应一个属性
#    num  outlook  temperature  humidity   windy   sport
# ------  -------  -----------  --------  ------  --------
#      1  sunny             85        85       0         0
#      2  sunny             80        90       1         0
#      3  overcast          83        78       0         1
#      4  rainy             70        96       0         1
#      5  rainy             68        80       0         1
#      6  rainy             65        70       1         0
#      7  overcast          64        65       1         1
#      8  sunny             72        95       0         0
#      9  sunny             69        70       0         1
#     10  rainy             75        80       0         1
#     11  sunny             75        70       1         1
#     12  overcast          72        90       1         1
#     13  overcast          81        75       0         1
#     14  rainy             71        80       1         0
# 计算条件属性的熵，例如天气，分三种情况（sunny，overcast，rainy）分别计算
# 气温80及以上定义为“hot”，70~80定义为“mid”，70以下定义为“cool”
# 湿度90及以上定义为“high”，70~90定义为“normal”
import math
import matplotlib.pyplot as plt
import numpy as np


def getExpectation(dataForm):  # 计算最后一列的信息期望
    numOfData = len(dataForm)  # 样本个数
    labelCounts = {}  # 用来统计属性及符合该属性的样本个数，例如{晴：2，多云：3，有雨：5}
    for eachData in dataForm:  # 遍历每行
        thisLabel = eachData[-1]  # 一行的最后一列
        if thisLabel not in labelCounts.keys():
            labelCounts[thisLabel] = 0  # 如果该属性还未出现过，则在字典labelCounts中添加该属性
        labelCounts[thisLabel] += 1
    thisException = 0.0
    for key in labelCounts:
        p = float(labelCounts[key]) / numOfData
        thisException -= p * math.log(p, 2)
    return thisException


def extractDataWithFeature(dataForm, axis, value):  # 按特征属性提取数据，axis是行号（对应特征，如天气outlook），value是要提取的具体属性值（如晴sunny）
    newDataForm = []
    for eachData in dataForm:
        if eachData[axis] == value:
            # singleData = eachData[:axis]
            # singleData.extend(eachData[axis:])
            newDataForm.append(eachData)
    return newDataForm


def chooseFeature(dataForm):
    numOfFeature = len(dataForm[0]) - 1  # numOfFeature即为属性的个数，减一是因为最后一列的属性是决策属性，并非条件属性
    decisionFeatureExpection = getExpectation(dataForm)
    bestGain = 0.0
    bestFeature = -1
    for i in range(numOfFeature):
        thisFeatureList = [example[i] for example in dataForm]  # 列表推导公式：c for b in a
        thisFeatureValue = set(thisFeatureList)  # set函数获取这个属性下的所有属性值
        thisfeatureExpection = 0.0
        for val in thisFeatureValue:  # 遍历这个属性下的所有属性值
            thisFeatureData = extractDataWithFeature(dataForm, i, val)  # 提取属性值为val的数据保存到thisFeatureData中
            p = len(thisFeatureData)/len(dataForm)
            thisfeatureExpection += p * getExpectation(thisFeatureData)
        thisFeatureGain = decisionFeatureExpection - thisfeatureExpection
        if thisFeatureGain > bestGain:
            bestGain = thisFeatureGain
            bestFeature = i
    return bestFeature  # 返回gain值最大的属性标号，int类型


def normalizeData(dataForm):
    for i in range(len(dataForm)):
        if dataForm[i][1] >= 80:
            dataForm[i][1] = 'hot'
        elif dataForm[i][1] >= 70:
            dataForm[i][1] = 'mid'
        else:
            dataForm[i][1] = 'cool'
        if dataForm[i][2] >= 90:
            dataForm[i][2] = 'high'
        elif dataForm[i][2] >= 70:
            dataForm[i][2] = 'normal'


def getTree(dataForm):
    normalizeData(dataForm)
    global bestFeatureName
    decisionList = [example[-1] for example in dataForm]
    if decisionList.count(decisionList[0]) == len(decisionList):
        return decisionList[0]
    bestFeature = chooseFeature(dataForm)
    if bestFeature == 0:
        bestFeatureName = 'outlook'
    if bestFeature == 1:
        bestFeatureName = 'temperature'
    if bestFeature == 2:
        bestFeatureName = 'humidity'
    if bestFeature == 3:
        bestFeatureName = 'windy'
    thisTree = {bestFeatureName: {}}
    for i in range(len(dataForm)):
        del(dataForm[i][bestFeature])  # 删除已经选过的属性
    featValue = [example[bestFeature] for example in dataForm]
    thisFeatureValue = set(featValue)
    for val in thisFeatureValue:
        thisTree[bestFeatureName][val] = getTree(extractDataWithFeature(dataForm, bestFeature, val))
    return thisTree


# boxstyle为文本框的类型，sawtooth是锯齿形，fc是边框线粗细,也可写作 decisionNode={boxstyle:'sawtooth',fc:'0.8'}
decisionNode=dict(boxstyle="sawtooth",fc="0.8")
# 定义决策树的叶子结点的描述属性
leafNode=dict(boxstyle="round4",fc="0.8")

# 定义决策树的箭头属性
arrow_args=dict(arrowstyle="<-")


# def plotNode(nodeTxt,centerPt,parentPt,nodeType):
#     # annotate是关于一个数据点的文本
#     ax1 = plt.subplots()
#     ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction', xytext=centerPt,textcoords='axes fraction',va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)


# 创建绘图
def createPlot():
    # 类似于Matlab的figure，定义一个画布(暂且这么称呼吧)，背景为白色
    fig, ax1 = plt.subplots()
    # createPlot.ax1为全局变量，绘制图像的句柄，subplot为定义了一个绘图，111表示figure中的图有1行1列，即1个，最后的1代表第一个图
    # 绘制结点

    ax1.annotate('决策节点', xy=(0.5, 0.1), xytext=(0.1, 0.5), arrowprops=arrow_args)
    # plotNode('叶节点',(0.8,0.1),(0.3,0.8), leafNode)
    # 显示画图
    plt.show()


createPlot()