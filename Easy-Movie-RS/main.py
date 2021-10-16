import os
import json
import random
import math


class MovieRec:
    def __init__(self, file_path, seed, k, n_items):
        self.file_path = file_path
        # self.users_1000 = self.__select_1000_users()
        self.seed = seed
        self.k = k
        self.n_items = n_items
        self.train, self.test = self.__load_and_split_data()

    def __load_and_split_data(self):
        train = dict()
        test = dict()
        if os.path.exists("data/train.json") and os.path.exists("data/test.json"):
            train = json.load(open("data/train.json"))
            test = json.load(open("data/test.json"))
            print("训练集和测试集加载完毕.")
            # print(train)
        else:
            random.seed(self.seed)
            for file in os.listdir(self.file_path):
                one_path = "{}/{}".format(self.file_path, file)
                print("{}".format(one_path))
                with open(one_path, "r") as fp:
                    movieID = fp.readline().split(":")[0]
                    for line in fp.readlines():
                        continue
                    userID, rate, _ = line.split(",")
                    # 判断用户是否在所选择的1000个用户中
                    if userID in self.users_1000:
                        if random.randint(1, 50) == 1:
                            test.setdefault(userID, {})[movieID] = int(rate)
                        else:
                            train.setdefault(userID, {})[movieID] = int(rate)
            print("加载完毕.")
            json.dump(train, open("data/train.json", "w"))
            json.dump(test, open("data/test.json", "w"))
        return train, test

    def pearson(self, rating1, rating2):
        sum_xy = 0
        sum_x = 0
        sum_y = 0
        sum_x2 = 0
        sum_y2 = 0
        num = 0
        for key in rating1.keys():
            if key in rating2.keys():
                num += 1
                x = rating1[key]
                y = rating2[key]
                sum_xy += x * y
                sum_x += x
                sum_y += y
                sum_x2 += math.pow(x, 2)
                sum_y2 += math.pow(y, 2)
        if num == 0:
            return 0
        denominator = math.sqrt(sum_x2 - math.pow(sum_x, 2) / num) * math.sqrt(sum_y2 - math.pow(sum_y, 2) / num)
        if denominator == 0:
            return 0
        else:
            return (sum_xy - (sum_x * sum_y) / num) / denominator

    def recommend(self, userID):
        neighborUser = dict()
        for user in self.train.keys():
            if userID != user:
                distance = self.pearson(self.train[userID], self.train[user])
                neighborUser[user] = distance
        # 字典排序
        newNU = sorted(neighborUser.items(), key=lambda k: k[1], reverse=True)

        movies = dict()
        for (sim_user, sim) in newNU[:self.k]:
            for movieID in self.train[sim_user].keys():
                movies.setdefault(movieID, 0)
                movies[movieID] += sim * self.train[sim_user][movieID]
        newMovies = sorted(movies.items(), key=lambda k: k[1], reverse=True)
        return newMovies


if __name__ == "__main__":
    file_path = "data"
    seed = 30 #随机种子
    k = 15 #选取的近邻用户个数
    n_items = 20 #推荐Top-n电影
    rec = MovieRec(file_path, seed, k, n_items)
    r = rec.pearson(rec.train["1282424"], rec.train["516722"])
    print("1282424 和 516722 的皮尔逊相关系数为:{}".format(r))
    result = rec.recommend("1282424")
    print("为用户1282424推荐的电影为：{}".format(result))