### 6주차 code1 fish_weight_knn

import numpy as np

#perch_length = np.array(
fish_length = np.array(
    [8.4, 13.7, 15.0, 16.2, 17.4, 18.0, 18.7, 19.0, 19.6, 20.0, 
     21.0, 21.0, 21.0, 21.3, 22.0, 22.0, 22.0, 22.0, 22.0, 22.5, 
     22.5, 22.7, 23.0, 23.5, 24.0, 24.0, 24.6, 25.0, 25.6, 26.5, 
     27.3, 27.5, 27.5, 27.5, 28.0, 28.7, 30.0, 32.8, 34.5, 35.0, 
     36.5, 36.0, 37.0, 37.0, 39.0, 39.0, 39.0, 40.0, 40.0, 40.0, 
     40.0, 42.0, 43.0, 43.0, 43.5, 44.0]
     )
fish_weight = np.array(
    [5.9, 32.0, 40.0, 51.5, 70.0, 100.0, 78.0, 80.0, 85.0, 85.0, 
     110.0, 115.0, 125.0, 130.0, 120.0, 120.0, 130.0, 135.0, 110.0, 
     130.0, 150.0, 145.0, 150.0, 170.0, 225.0, 145.0, 188.0, 180.0, 
     197.0, 218.0, 300.0, 260.0, 265.0, 250.0, 250.0, 300.0, 320.0, 
     514.0, 556.0, 840.0, 685.0, 700.0, 700.0, 690.0, 900.0, 650.0, 
     820.0, 850.0, 900.0, 1015.0, 820.0, 1100.0, 1000.0, 1100.0, 
     1000.0, 1000.0]
     )

from sklearn.model_selection import train_test_split

# 훈련 세트와 테스트 세트로 나눕니다
train_input, test_input, train_target, test_target = train_test_split(
    fish_length, fish_weight, random_state=42)
# 훈련 세트와 테스트 세트를 2차원 배열로 바꿉니다
train_input = train_input.reshape(-1, 1)
test_input = test_input.reshape(-1, 1)

# k-최근접 이웃 회귀 모델을 불러옵니다
from sklearn.neighbors import KNeighborsRegressor

knr = KNeighborsRegressor(n_neighbors=3)
# k-최근접 이웃 회귀 모델을 훈련합니다
knr.fit(train_input, train_target)

# 예측할 농어의 길이를 입력받습니다.
check_length = float(input("무게를 예측할 농어의 길이를 입력하세요 (5 ~ 45) : "))

print(f"k-최근접 이웃 회귀 모델을 이용하여 {check_length}cm 농어의 무게를 예측해보겠습니다.")
estimate_weight = np.round(knr.predict([[check_length]]), 1)

print(f"길이가 {check_length}cm인 농어의 무게는 인접한 데이터를 이용한 결과", estimate_weight,"g로 예상됩니다.")
print("예측 그래프는 아래와 같습니다.")

import matplotlib.pyplot as plt

# 입력받은 농어의 이웃을 구합니다
distances, indexes = knr.kneighbors([[check_length]])

# 훈련 세트의 산점도를 그립니다
plt.scatter(train_input, train_target)
# 훈련 세트 중에서 이웃 샘플만 다시 그립니다
print(f"{check_length}cm 농어와 이웃한 데이터는 주황색 다이아몬드로 표시하였습니다.")
plt.scatter(train_input[indexes], train_target[indexes], marker='D')
# 입력받은 농어 데이터
plt.scatter(check_length, estimate_weight, marker='^')
plt.xlabel('length')
plt.ylabel('weight')
plt.show()