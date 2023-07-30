### 6주차 code4 fish_weight_poly.py
### 다항 회귀 방법을 이용한 예측 
print("다항 회귀 방법을 이용하여 예측해보겠습니다.(2차 방정식)")
train_poly = np.column_stack((train_input ** 2, train_input))
test_poly = np.column_stack((test_input ** 2, test_input))

# 데이터 셋 크기 출력
#print(train_poly.shape, test_poly.shape)

lr = LinearRegression()
lr.fit(train_poly, train_target)

# 예측할 농어의 길이를 입력받습니다.
check_length = float(input("무게를 예측할 농어의 길이를 입력하세요 (100 이상도 가능) : "))
print(f"다항 회귀 모델을 이용하여 {check_length}cm 농어의 무게를 예측해보겠습니다.")

estimate_weight = np.round(lr.predict([[check_length**2, check_length]]), 1)

print(f"길이가 {check_length}cm인 농어의 무게는 다항 회귀 모델을 이용한 결과", estimate_weight,"g로 예상됩니다.")
print("계산 공식은 아래와 같습니다.")
print(f'농어무게 = ({np.round(lr.coef_[0], 1)}) x 농어길이**2 + ({np.round(lr.coef_[1], 1)}) x 농어길이 + ({np.round(lr.intercept_, 1)})')

print("예측 그래프는 아래와 같습니다.")
print("선형 회귀 모델보다는 적정하게 예측합니다.")


# 구간별 곡선을 그리기 위해 5에서 입력받은 숫자까지 정수 배열을 만듭니다
point = np.arange(5, check_length)
# 훈련 세트의 산점도를 그립니다
plt.scatter(train_input, train_target)
# 5에서 입력받은 숫자까지 2차 방정식 그래프를 그립니다
plt.plot(point, lr.coef_[0]*point**2 + lr.coef_[1]*point + lr.intercept_)
# 입력받은 농어 데이터
plt.scatter([check_length], [estimate_weight], marker='^')
plt.xlabel('length')
plt.ylabel('weight')
plt.show()
