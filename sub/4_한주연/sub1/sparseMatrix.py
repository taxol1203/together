import itertools
from collections import Counter
from parse import load_dataframes
from analyze import sort_stores_by_score
from analyze import get_most_active_users
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import scipy

def user_store_dataFrame_to_csrMatirx(df):

    users_reviews = pd.merge(
        df["users"], df["reviews"], left_on="id", right_on="user"
    )
    # users_reviews.pivot(index="user", columns="store", values="score")
    # "ValueError: Index contains duplicate entries, cannot reshape" 발생 함
    # why: 같은 users와 store 가진 score 값이 2개 이상 중복이 가지게 됨
    # -> pd.pivot_table을 사용 
    UR_pivots = users_reviews.pivot_table(index="user", columns="store", values="score", aggfunc=np.mean)

    # Pivot table을 Pandas Sparse 행렬 데이터 타입으로 저장하였다.
    # 기존의 Sparse Matrix의 데이터 크기는 엄청나게 크다. 따라서 효율적으로 SparseDtype이라는 type을 사용하여 효율을 높인다.
    # 매개변수의 "int"와 "np.nan"은 데이터가 있는 곳은 int로, 없는 곳을 np.nan을 만든다는 뜻이다.
    # SparseDtype으로 변경하면 메모리 효율이 엄청나게 올라간다. 6.5GB -> 1.5MB
    UR_pivots_sparseType = UR_pivots.astype(pd.SparseDtype("int", np.nan))

    # pivots dataframe을 sparse Matrix로 만든다
    # pivots table에는 NaN 값이 너무 많아 이를 값이 있는 인덱스와 그의 값으로 나타내는 1차원 배열 3개로 압축한다.
    # UR_pivots에는 NaN 값이 들어있는데, csr_matrix은 이를 인식하지 못하므로, fillna(0)을 통해 NaN을 0으로 교체한다. 
    # sparseM = scipy.sparse.csr_matrix(UR_pivots.fillna(0).values)
    sparseM = scipy.sparse.csr_matrix(UR_pivots_sparseType.fillna(0).values)

    print(sparseM.indptr)   # 행렬의 '0'이 아닌 원소의 행의 시작 위치
    print(sparseM.indices)  # 행렬의 '0'이 아닌 원소의 열의 위치
    print(sparseM.data)     # 행렬의 '0'이 아닌 원소 값

    # 검증 : 위에서 만든 sparseM에의 각 인덱스를 넣어보아, UR_pivots의 data와 spareseM의 data가 같은지 확인
    print(UR_pivots.iloc[0,16262])  

def user_category_sparse_to_csrMatrix(df):
    
    stores = df["stores"][["id","category","review_cnt"]]

    stores = stores[(stores["category"] != "") & (stores["review_cnt"] > 0)]

    stores["category"] = stores["category"].str.split("|")

    stores = stores.explode("category")

    reviews = df["reviews"][["store", "user", "score"]]
    # 필요한 컬럼만 남긴다("store", "user", "score")

    stores_reviews = pd.merge(stores, reviews, left_on="id", right_on="store")
    # store와 review 데이터 프레임을 합친다.

    grouped = stores_reviews.groupby(["user", "category"])["score"].mean().reset_index(name="score")
    # user_id와 category를 기준으로 그룹화한다.
    # score 컬럼의 평균을 score에 저장한다.

    sr_pivot_table = grouped.pivot_table(index="user", columns="category", values="score")
    # pivot_table로 2개의 축을 갖는 행렬로 만든다.

    uc_pivot_sparsetype = sr_pivot_table.astype(pd.SparseDtype("float", np.nan))
    # 내부 데이터의 타입을 변환시킨다.

    sparseM = scipy.sparse.csr_matrix(sr_pivot_table[0:100].fillna(0).values)

    print(sparseM.indptr)   # 행렬의 '0'이 아닌 원소의 행의 시작 위치
    print(sparseM.indices)  # 행렬의 '0'이 아닌 원소의 열의 위치
    print(sparseM.data)     # 행렬의 '0'이 아닌 원소 값
    pass

def main():
    data = load_dataframes()
    user_store_dataFrame_to_csrMatirx(data)
    # user_category_sparse_to_csrMatrix(data)
    
if __name__ == "__main__":
    main()