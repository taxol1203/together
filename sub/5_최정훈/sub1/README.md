# [Pandas, Python]


`apply` : DataFrame에서 복수 개의 컬럼이 필요할 때 사용.

`lambda` : 익명 함수 (간단한 사칙연산이나, 문자열 추출에 `lambda` 를 적용한 apply 함수가 좋다.

- 표현 방법 : ``` lambda

`itertools` : 효율적인 반복을 위한 함수

- chain.from_iterable() : chain.from_iterable(['ABC', 'DEF']) → A B C D E F
Arguments : iterable (반복 가능한 객체) → list, dict, set, str, tuple,range ...

`filter` : 특정 조건으로 걸러서 걸러진 요소들로 `iterator` 객체를 만들어서 리턴해줌. `map` 함수와 사용방 법은 동일하나, 함수의 결과가 참인지 거짓인지에 따라, 해당 요소를 포함할 지 결정함.

```python
filter(적용시킬 함수, 적용할 요소들)
```

`Counter` : 컨테이너등에 동일한 자료가 몇 개인지를 확인하는데 사용하는 객체

`list` : list로 변환한다.

`most_common` : 최빈값을 구함.

### Seaborn

`countplot` : 항목별 갯수를 세어주는 차트 → 알아서 해당 column을 구성하고 있는 value들을 구분하여 보여줌.

`set_xticklabels` : x축에 대한 사용자 지정 눈금 레이블을 설정할 수 있게하는 함수

```python
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"])
```

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/d4f63277-2c16-4088-8ad5-59fa64139adc/Untitled.png)

`rotation` : 눈금의 크기를 지정할 수 있음.

```python
ax.set_xticklabels(ax.get_xticklabels(),rotation = 30, size = 10)
# 눈금 30으로 지정함
```

## Req. 4-1.

### 희소행렬(sparse matrix)

행렬의 값이 대부분 0인 경우를 가리키는 표현.

sparse matrix는 대부분의 행렬의 값이 0이기 때문에 연산 시 필요없는 부분이 상당히 많습니다. 따라서 행렬 연산에 수많은 0을 연산하는 것은 비효율적인 뿐 아니라 계산에서도 비효율적입니다. 

sparse matrix를 좀 더 효율적으로 관리하기 위한 방법이 필요합니다. sparse matrix를 저장하기 위한 다양한 방법이 존재하는데, 그 중 CSR(Comporessed Sparse Row) 또는 CRS(Compressed Row Storage)로 불리는 저장 방법이 있습니다.

이 방법은 **3개의 벡터를 이용하여 행렬을 표현합니다.** 각 벡터를 `DATA` `Row` `Col` 이라고 부르겠습니다.