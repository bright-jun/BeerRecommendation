import numpy as np

class Transform:
    def __init__(self,array,beer_group,usernum):
        self.user_beer = array
        """self.user_beer = ([[0,0,5],
                       [0,1,1],
                       [0,2,0],
                       [0,3,4],
                       [0,4,5],
                       [1,0,1],
                       [1,1,1],
                       [1,2,4],
                       [1,3,5],
                       [1,4,5],
                       [2,0,5],
                       [2,1,5],
                       [2,2,4]])
        """
        self.beer_group = beer_group
        #self.beer_group = ([1,1,2,3,3])
        self.user_group = np.zeros([usernum,19])
        self.user_group_div = np.ones([usernum,19])
        
    def transform(self):
        #user_beer[i][2] rating
        for i in range(len(self.user_beer)):
        #user_beer[i][0] user
        #user_beer[i][1] beer
            self.user_group[self.user_beer[i][0]][self.beer_group[self.user_beer[i][1]-1]-1] += self.user_beer[i][2]
            self.user_group_div[self.user_beer[i][0]][self.beer_group[self.user_beer[i][1]-1]-1] += 1000
            
            #그룹에 포함된 맥주 갯수만큼 각각 나눠주어야 함
        self.user_group = (self.user_group*1000)/self.user_group_div