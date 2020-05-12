import numpy as np

class Group:
    def __init__(self, beer_group, user_beer):
        self.beer_group = beer_group
        self.user_beer = user_beer
        self.beers = None

    def user(self, user_id):
        list = []
        for i in self.user_beer:
            if i[0] == user_id:
                list.append([i[1],i[2]])

        return list

    def group(self, group_index):
        list = []
        for i in range(len(self.beer_group)):
            if self.beer_group[i] == group_index:
                list.append([i+1, 0])

        return list

    def user_group(self, user_id, group_index, reverse=True):
        group_beers = self.group(group_index)
        user_beers = self.user(user_id)
        reverse = reverse

        for i in group_beers:
            for j in user_beers:
                if i[0]==j[0]:
                    i[1]=j[1]

        return sorted(group_beers, key=lambda k: k[1], reverse=reverse)