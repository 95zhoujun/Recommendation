critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snake on a Plane': 3.5,
                         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                         'The Night Listener': 3.0},

           'Gene Seymour': {'Lady in the Water': 3.0, 'Snake on a Plane': 3.5,
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5, },

           'Michael Phillips': {'Lady in the Water': 2.5, 'Snake on a Plane': 3.0,
                                'Superman Returns': 3.5, 'The Night Listener': 4.0},

           'Claudia Puig': {'Snake on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                            'You, Me and Dupree': 2.5},

           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snake on a Plane': 4.0,
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0},

           'Jack Matthews': {'Lady in the Water': 3.0, 'Snake on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},

           'Toby': {'Snake on a Plane': 4.5, 'You, Me and Dupree': 1.0, 'Superman Returns': 4.0}}

from math import sqrt


# 返回一个有关 person1 和 person2 的基于距离的相似度评价
def sim_distance(prefs, person1, person2):
    # 得到 shared_items 的列表
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    # 如果没有共同之处，返回 0
    if len(si) == 0: return 0

    # 计算所有差值的平方和
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sqrt(sum_of_squares))


# 返回 p1 和 p2 的皮尔逊相关系数
def sim_pearson(prefs, p1, p2):
    # 得到双方都曾评价过的物品列表
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]: si[item] = 1

    # 得到 si 列表元素的个数
    n = len(si)

    # 如果两者没有共同之处，返回 1
    if n == 0: return 1

    # 对所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # 求平方和
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    # 求乘积和
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # 计算皮尔逊评价值
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    r = num / den

    return r


# 从反映偏好的字典中返回最为匹配者
# 返回结果的个数和相似度函数均为可选参数
def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]
    # 参见列表推导式
    # 对列表排序，评价值最高的排在前面
    scores.sort()  # 排序
    scores.reverse()  # 反向列表中元素
    return scores[0:n]


# 利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # 不要和自己作比较
        if other == person: continue
        sim = similarity(prefs, person, other)
        # 忽略评价值为零或小于零的情况
        if sim <= 0: continue
        for item in prefs[other]:
            # 只对自己还没看过的影片评价
            if item not in prefs[person] or prefs[person][item] == 0:
                # 相似度 * 评价值
                totals.setdefault(item, 0)
                # setdefault() 函数: 如果键不已经存在于字典中，将会添加键并将值设为默认值。
                # dict.setdefault(key, default=None)
                # key -- 查找的键值。
                # default -- 键不存在时，设置的默认键值。
                totals[item] += prefs[other][item] * sim
                # 相似度之和
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # 建立一个归一化的列表
    rankings = [(total / simSums[item], item) for item, total in totals.items()]  # 列表推导式
    # 返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings


# 这个函数就是将字典里面的人员和物品对调
def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # 将物品和人员对调
            result[item][person] = prefs[person][item]
    return result


def calculateSimilarItems(prefs, n=10):
    # 建立字典，以给出与这些物品最为相近的所有其他物品
    result = {}
    # 以物品为中心对偏好矩阵实施倒置处理
    itemPrefs = transformPrefs(prefs)
    c = 0
    for item in itemPrefs:
        # 针对大数据集更新状态变量
        c += 1
        #print(len(itemPrefs))
        if c % 100 == 0: print("%d / %d" % (c, len(itemPrefs)))
        # 寻找最为相近的物品
        scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result  # 返回一个包含物品及其最相近物品列表的字典


def getRecommendedItems(prefs, itemMatch, user):
    userRatings = prefs[user]
    scores = {}
    totalSim = {}
    # 循环遍历由当前用户评分的物品
    for (item, rating) in userRatings.items():  # dict.items() 此方法返回元组对的列表。
        # 寻遍遍历与当前物品相机的物品
        for (similarity, item2) in itemMatch[item]:
            # 如果该用户已经对当前物品做过评价，则将其忽略
            if item2 in userRatings: continue
            # 评价值与相似度的加权之和
            scores.setdefault(item2, 0)  # setdefault 见前面注释
            scores[item2] += similarity * rating
            # 全部相似度之和
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity
        # 将每个合计值除以加权和，求出平均值
    rankings = [(score / totalSim[item], item) for item, score in scores.items()]
    # 按最高值到最低值的顺序，返回评分结果
    rankings.sort()
    rankings.reverse()
    return rankings


def loadMovieLens(path='./data/my-small'):
    import csv
    # 获取影片标题
    movies = {}
    for line in open(path + '/movies.csv'):
        (id, title) = line.split('\t')[0:2]  # 这里文件中第三列是影片类型，略作修改
        movies[id] = title  # 把 title 和 id对应
    # 加载数据
    prefs = {}
    with open('./data/my-small/ratings.csv') as csv_file:
        row = csv.reader(csv_file,delimiter=',')
        next(row) #读取首行
        ratings = [] #建立一个数组来存储评价数据
        #读取除首行之后每一行的的3列数据，并将其加入到数组ratings之中
        for r in row:
            ratings.append(float(r[2])) #将字符串转换为浮点型加入到数组之中
    #print(len(ratings))
    #print(ratings[0])
    #print(ratings[100835])
    i = 0
    for line in open(path + '/ratings.csv'):
        if(i==len(ratings)): break
        (user, movieid, rating, ts) = line.split(',')  # 分割
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = ratings[i]
        i+=1
        #print(i)
    return prefs