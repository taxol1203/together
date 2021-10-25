import pandas as pd
import numpy as np
import itertools
from collections import Counter
from os import name
from parse import load_dataframes
from scipy import sparse
import scipy


def get_user_store(dataframes):
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    # user id에서 중복되는 값 제거
    user_list = list(set(stores_reviews["user"].values.tolist()))
    # user id 오름차순 정렬
    user_list.sort()
    # store name에서 중복되는 값 제거
    store_list = list(set(stores_reviews["store_name"].values.tolist()))
     # 유저와 음식점을 축으로 평점을 값은 nan으로 설정 후 dataframe 생성
    df = pd.DataFrame(data=np.nan, index=user_list, columns=store_list)
    
    # 유저 id와 가게이름으로 grouping 후 평균을 내고 그 중 score 값을 남긴다.
    user_group = stores_reviews.sort_values(by='user').groupby(["user", "store_name"]).mean().loc[:, "score"]
    # i = (user_id, store_name) 이 score = 평점
    for i, score in user_group.items():
        user, store_name = i
        # df에서 행에서는 유저 id를 열에서는 가게 이름을 찾아 nan값을 평점으로 변경한다.
        df.loc[user,  store_name] = score
    # df를 sparseDtype으로 변경
    sdf = df.astype(pd.SparseDtype("float", np.nan))
    
    print(df.info())
    print("---------------------")
    print(sdf.info())


# 유저-카테고리 행렬
# 유저와 음식점 카테고리를 축으로 하고 평점 평균을 값으로 갖는 행렬을 만듦
def get_user_category(dataframes):
    # stores_reviews = pd.merge(
    #     dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    # )

    # user_list = list(set(stores_reviews["user"].values.tolist()))
    # user_list.sort()
    # category_list = stores_reviews["category"].str.split("|")
    # category_list = category_list.explode("category")
    # df = pd.DataFrame(data=np.nan, index=user_list, columns=category_list)
   


    # 카테고리 | 로 구분되어 있는거를 리스트로 넣어줘야한다
    stores = dataframes["stores"][["id","category", "review_cnt"]]
    # category 가 없거나 review가 없는 음식점 제거.
    stores = stores[(stores["category"] != "") & (stores["review_cnt"] > 0)]
    # 구분자("|") 로 구분되어 있는 category를 리스트 형태로 변환한다.
    stores["category"] = stores["category"].str.split("|")
    # category를 기준으로 row를 분리함
    stores = stores.explode("category")

    reviews = dataframes["reviews"][["store", "user", "score"]]
    stores_reviews = pd.merge(stores, reviews, left_on="id", right_on="store")
    grouped_stores_reviews = stores_reviews.groupby(["user", "category"])["score"].mean().reset_index(name="score")

    uc_pivot_table = grouped_stores_reviews.pivot_table(index="user", columns="category", values="score")
#     print(uc_pivot_table.info())
#     print("---------------------------------------")
    uc_pivot_sparsetype = uc_pivot_table.astype(pd.SparseDtype("float", np.nan))
    
    csr_matrix = scipy.sparse.csr_matrix(uc_pivot_sparsetype)
#     print(uc_pivot_sparsetype.info())
    return csr_matrix

def main():
    data = load_dataframes()
#     get_user_store(data)
    get_user_category(data)

if __name__ == "__main__":
    main()
