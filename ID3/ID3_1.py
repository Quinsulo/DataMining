# 决策属性“适不适合运动”，结果分两类，适合/不适合
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
import mathTool
trainData = [
    ['sunny', 85, 85, 0, 0],
    ['sunny', 80, 90, 1, 0],
    ['overcast', 83, 78, 0, 1],
    ['rainy', 70, 96, 0, 1],
    ['rainy', 68, 80, 0, 1],
    ['rainy', 65, 70, 1, 0],
    ['overcast', 64, 65, 1, 1],
    ['sunny', 72, 95, 0, 0],
    ['sunny', 69, 70, 0, 1],
    ['rainy', 75, 80, 0, 1],
    ['sunny', 75, 70, 1, 1],
    ['overcast', 72, 90, 1, 1],
    ['overcast', 81, 75, 0, 1],
    ['rainy', 71, 80, 1, 0]
]

myTree = mathTool.getTree(trainData)
