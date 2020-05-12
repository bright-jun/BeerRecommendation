# CollaborativeFiltering

## Main.py
- 서비스를 제공해주는 코드입니다.
- getRecommendation(userid)
	- user의 선호하는 그룹을 정렬해서 추천해줍니다.
- group.user_group(userid,group_index,reverse)
	- user의 group에 포함된 맥주들을 선호도를 기반으로 정렬해서 추천해줍니다.

## Group.py
- 유저별 group의 맥주들을 관리하기 위한 함수를 작성한 코드입니다.

## Transform.py
- User-Beer rating을 User-Group rating으로 바꿔주는 함수를 작성한 코드입니다.

## Collaborative.py
- Collaborative Filtering을 이용한 추천 함수를 작성한 코드입니다.
- Pearson 상관계수를 기준으로 유사도를 측정합니다
- User-based 방식으로 Collaborative Filtering을 진행합니다.