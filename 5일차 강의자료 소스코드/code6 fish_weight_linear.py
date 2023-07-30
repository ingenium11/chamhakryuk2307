### 6주차 code3 fish_weight_linear.py
### 선형 회귀 방법을 이용한 예측
print("선형 회귀 방법을 이용하여 예측해보겠습니다.")
from sklearn.linear_model import LinearRegression

lr = LinearRegression()
# 선형 회귀 모델 훈련
lr.fit(train_input, train_target)

# 예측할 농어의 길이를 입력받습니다.
check_length = float(input("무게를 예측할 농어의 길이를 입력하세요 (100 이상도 가능) : "))
print(f"{check_length}cm 농어의 무게를 예측해보겠습니다.")

# 입력받은 농어에 대한 예측
print(f"선형 회귀 모델을 이용하여 {check_length}cm 농어의 무게를 예측해보겠습니다.")
estimate_weight = np.round(lr.predict([[check_length]]), 1)

print(f"길이가 {check_length}cm인 농어의 무게는 선형 회귀 모델을 이용한 결과", estimate_weight,"g로 예상됩니다.")
print("계산 공식은 아래와 같습니다.")
print(f'농어무게 = ({np.round(lr.coef_, 1)}) x 농어길이 + ({np.round(lr.intercept_, 1)})')

print("예측 그래프는 아래와 같습니다.")
print("k-최근접 이웃 회귀 모델보다는 적정하게 예측합니다.")
print("하지만 농어의 무게가 0g 이하로 내려갈 수도 있는 비현실적인 예측이 발생할 수 있습니다.")

# 훈련 세트의 산점도를 그립니다
plt.scatter(train_input, train_target)
# 5에서 입력받은 숫자까지 1차 방정식 그래프를 그립니다
plt.plot([5, check_length], [5*lr.coef_+lr.intercept_, check_length*lr.coef_+lr.intercept_])
# 입력받은 농어 데이터
plt.scatter(check_length, estimate_weight, marker='^')
plt.axhline(color='k', linestyle=':')
plt.axvline(color='k', linestyle=':')
plt.xlabel('length')
plt.ylabel('weight')
plt.show()