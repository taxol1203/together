from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
import re
import pandas as pd
import time
import os
import pickle

# 영화의 Overview(개요)의 연관성을 통해 영화를 추천해 준다.
def recommend(movie_name):
    # -------- Load Dataset -----------
    try:
        movies = pickle.load(open("movie_cbf_rec_df.pickle", "rb"))
    except (OSError, IOError) as e:
        # movie json을 dataframe으로 만들기
        dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'  # 절대 경로로 설정 함 -> 나중에 서버에 올리면 문제가 되지 않을까?
        with open(dir + '../data/movies_kr.json', 'r') as f:
            data = json.loads(f.read())
        df_nested_list = pd.json_normalize(data)

        # 필요한 필드
        movies = df_nested_list[["pk", "fields.original_title", "fields.overview", "fields.vote_count"]]
        movies = movies.rename(columns={'pk': 'movieId'})
        movies = movies.rename(columns={'fields.original_title': 'original_title'})
        movies = movies.rename(columns={'fields.overview': 'overview'})
        movies = movies.rename(columns={'fields.vote_count': 'vote_count'})

        movies["overview"] = movies["overview"].astype("str")
        # 줄거리가 NaN인 영화 drop
        movies.dropna()

        # "overview" column 모두 소문자로, 문자+숫자만 남기고 나머지는 띄어쓰기로 대체
        movies["overview"] = movies["overview"].apply(lambda x : re.sub("\W", " ", x.lower()))
        pickle.dump(movies, open("movie_cbf_rec_df.pickle", "wb"))


    # TF-IDF 기반으로 단어 벡터화
    tfidf_vec = TfidfVectorizer(ngram_range=(1, 2)) # Vectorizer생성   # ngram_range=(1, 2)는 단어를 1개 혹은 2개 연속으로 보겠다는 뜻
    tfidf_matrix = tfidf_vec.fit_transform(movies["overview"]) # Vectorizer가 단어들을 학습

    plot_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix) # 줄거리 간 cosine 유사도 구하기
    # print("### COSINE Similarity ###")
    # print(plot_similarity)
    similar_index = np.argsort(-plot_similarity) # 유사도 높은 순서대로 index 정렬
    # print("### 유사도 기준 index 정렬 ###")
    # print(similar_index)

    input_movie = movie_name  # data에 있는 영화의 제목 입력

    movie_index = movies[movies["original_title"] == input_movie].index.values # input_movie에 해당하는 index 값 가져오기
    similar_movies = similar_index[movie_index, :100]    # 유사도 상위 100개 index 가져오기
    # 인덱스로 사용하기 위해서는 1차원으로 변형
    similar_movies_index = similar_movies.reshape(-1)   # similar_movies 1차원 변형
    # 해당하는 인덱스에 대한 영화 정보들을 가져온다.
    movies = movies.iloc[similar_movies_index]
    # 1000개 미만 평가를 받은 영화는 제외한다.
    movies = movies[movies["vote_count"] >= 1000]
    print(movies.head(10))  # 유사도 상위 10개 영화 가져오기
    result = []
    cnt = 0
    for movie_id in movies['movieId']:
        if cnt == 0:    # 제일 처음 나오는 영화는 중복이므로 넘긴다.
            cnt += 1
            continue
        if cnt == 11:   # 10개의 추천 영화를 제공한다.
            break
        result.append(movie_id)
        cnt += 1

    return result


if __name__ == '__main__':
    movie_name = "Iron Man"     # 영화 이름 지정
    start = time.time()  # 시작 시간 저장
    recommend(movie_name)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간