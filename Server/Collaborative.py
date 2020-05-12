import numpy as np
from math import sqrt

class Collaborative:
    def __init__(self,userCluster):
        self.userCluster = userCluster
        """
        self.userCluster = ([[4,0,0,2,4,0,0,0,4,5,1,5,0,4,0,4,3,5,0]]) # colume = number of cluster
        self.userCluster = np.append(self.userCluster, [[3,0,4,3,4,0,0,2,3,4,0,2,3,4,5,1,2,0,0]], axis = 0)
        self.userCluster = np.append(self.userCluster, [[4,3,0,3,5,1,5,0,2,5,0,0,0,0,5,0,0,2,0]], axis = 0)
        self.userCluster = np.append(self.userCluster, [[0,2,3,5,0,0,3,2,0,0,0,0,1,0,5,0,4,4,0]], axis = 0)
        self.userCluster = np.append(self.userCluster, [[0,3,4,3,5,1,5,0,3,5,5,0,0,0,4,0,0,0,3]], axis = 0)
        """

        self.li = []

    def sim_distance(self, beer1, beer2):
        sum = 0
        for i in range(len(beer1)):
            if beer1[i] * beer2[i] != 0: # Same beer rating
                sum += pow(beer1[i] - beer2[i],2)
        return 1/(1+sqrt(sum))

    def sim_pearson(self, beer1, beer2):
        sumX = 0 # SUM OF X
        sumY = 0 # SUM OF Y
        sumPowX = 0 # SUM of X^2
        sumPowY = 0 # SUM of Y^2
        sumXY = 0 # SUM of X*Y
        count = 0 # NUMBER of BEER

        for i in range(len(beer1)):
            if beer1[i] * beer2[i] != 0: # Same beer rating
                sumX += beer1[i]
                sumY += beer2[i]
                sumPowX += pow(beer1[i], 2)
                sumPowY += pow(beer2[i], 2)
                sumXY += beer1[i] * beer2[i]
                count += 1

        if count<=1:
            return 0
        else:
            return ( sumXY - ((sumX * sumY)/count)) / sqrt((sumPowX - (pow(sumX,2) / count )) * (sumPowY - (pow(sumY,2)/count)))

    def top_match(self, uid, index=3):
        for i in range(len(self.userCluster)):
            if uid != i:
                self.li.append((self.sim_pearson(self.userCluster[uid],self.userCluster[i]),i))

        return self.li[:index]

    def getRecommendation(self, uid):
        result = self.top_match(uid, len(self.userCluster))

        simSum=0
        score=0
        self.li=np.zeros(len(self.userCluster[0]))


        for sim,name in result:
            if sim<0 : continue
            simSum+=sim
            for beer in range(len(self.userCluster[uid])):
                if self.userCluster[uid][beer]==0 :
                    self.li[beer]+=sim*self.userCluster[name][beer]
                else:
                    self.li[beer]= self.userCluster[name][beer]

        for beer in range(len(self.userCluster[uid])):
                if self.userCluster[uid][beer]==0 :
                    self.li[beer]/= simSum 

        self.li = self.li.tolist()
        #self.li.index(max(self.li))
        rank = sorted(range(len(self.li)), key=lambda k: self.li[k], reverse=True)
        rank = np.array(rank)+1
        #print(self.li)
        #print("#sorted#")
        #print(sorted(self.li,reverse=True))

        self.li = []
        return rank
