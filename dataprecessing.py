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

def test(path='./data/my-small'):
    import numpy as np
    import csv
    with open('./data/my-small/ratings.csv') as csv_file:
        row = csv.reader(csv_file,delimiter=',')
        next(row) #读取首行
        ratings = [] #建立一个数组来存储评价数据
        #读取除首行之后每一行的的3列数据，并将其加入到数组ratings之中
        for r in row:
            ratings.append(float(r[2])) #将字符串转换为浮点型加入到数组之中

        print(ratings[0:30])

prefs=loadMovieLens()
print(prefs['87'])