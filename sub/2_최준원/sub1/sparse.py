from parse import load_dataframes
import pandas as pd
import shutil
import numpy as np
import scipy
from scipy import sparse
import itertools

def users_reviews_csr_matrix(dataframes):
    """
    Req. 1-4-1 유저 - 음식점 행렬 생성
    """
    users = dataframes['users']
    reviews = dataframes['reviews']
    merge = pd.merge(
        users, reviews, left_on='id', right_on='user'
    )[:10000]

    # pivot table 생성
    pivot_table = merge.pivot_table(index='user', columns='store', values='score', aggfunc=np.mean, fill_value=0)

    # sparse dtype으로 변경
    pivot_sparse = pivot_table.astype(pd.SparseDtype('int'))

    # Compressed sparsed row Matrix로 변환하여 리턴
    csr_matrix = scipy.sparse.csr_matrix(pivot_sparse)

    print('-- Compressed sparse row --')
    # 행렬의 0이 아닌 원소의 행의 시작 위치
    print('indptr: ' , csr_matrix.indptr)
    # 행렬의 0이 아닌 원소의 열의 위치
    print('indices: ' , csr_matrix.indices)
    # 행렬의 0이 아닌 원소 값
    print('data: ' , csr_matrix.data)
    # 값이 잘 찍히는걸 볼 수 있다.
    print(csr_matrix[0, 39])
    return csr_matrix

def users_stores_csr_matrix(dataframes):
    stores = dataframes["stores"][['id', 'category', 'review_cnt']]
    # 카테고리가 없거나 리뷰가 없는 가게는 제거
    stores = stores[(stores['category'] != "") & (stores['review_cnt'] > 0)]
    stores['category'] = stores['category'].str.split('|')

    # category를 explode로 해서 열을 폭발시켜 줘야 한다
    stores = stores.explode('category')

    reviews = dataframes["reviews"][['store', 'user', 'score']]

    merge = pd.merge(
        stores, reviews, left_on='id', right_on='store'
    )
    # user id, category, avg_score를 컬럼으로 하는 새로운 df 생성
    # 리스트 형태로 된 category를 explode 하지 않고 groupby할 경우,
    # TypeError: unhashable type: 'list' 발생
    gp = merge.groupby(['user', 'category'])['score'].mean().reset_index(name='avg_score')

    # pivot table 생성
    pivot_table = gp.pivot_table(index='user', columns='category', values='avg_score')

    # sparse dtype으로 변경
    pivot_sparse = pivot_table.astype(pd.SparseDtype('float'))

    # Compressed sparsed row Matrix로 변환하여 리턴
    csr_matrix = scipy.sparse.csr_matrix(pivot_sparse)
    return csr_matrix

def main():
    df = load_dataframes()
    users_reviews_csr_matrix(df)
    # users_stores_csr_matrix(df)

if __name__ == "__main__":
    main()
