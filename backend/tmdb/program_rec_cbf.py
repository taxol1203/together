from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import numpy as np
import re
import pandas as pd
import time


# 영화의 Overview(개요)의 연관성을 통해 영화를 추천해 준다.
def recommend(program_name):
    # -------- Load Dataset -----------
    # program json을 dataframe으로 만들기
    with open('data/programs.json', 'r') as f:
        data = json.loads(f.read())
    df_nested_list = pd.json_normalize(data)

    # 필요한 필드
    programs = df_nested_list[["pk", "fields.original_title", "fields.overview", "fields.vote_count"]]
    programs = programs.rename(columns={'pk': 'programId'})
    programs = programs.rename(columns={'fields.original_title': 'original_title'})
    programs = programs.rename(columns={'fields.overview': 'overview'})
    programs = programs.rename(columns={'fields.vote_count': 'vote_count'})

    programs["overview"] = programs["overview"].astype("str")
    # 줄거리가 NaN인 영화 drop
    programs.dropna()

    # "overview" column 모두 소문자로, 문자+숫자만 남기고 나머지는 띄어쓰기로 대체
    programs["overview"] = programs["overview"].apply(lambda x : re.sub("\W", " ", x.lower()))

    # TF-IDF 기반으로 단어 벡터화
    tfidf_vec = TfidfVectorizer(ngram_range=(1, 2)) # Vectorizer생성   # ngram_range=(1, 2)는 단어를 1개 혹은 2개 연속으로 보겠다는 뜻
    tfidf_matrix = tfidf_vec.fit_transform(programs["overview"]) # Vectorizer가 단어들을 학습

    plot_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix) # 줄거리 간 cosine 유사도 구하기
    # print("### COSINE Similarity ###")
    # print(plot_similarity)
    similar_index = np.argsort(-plot_similarity) # 유사도 높은 순서대로 index 정렬
    # print("### 유사도 기준 index 정렬 ###")
    # print(similar_index)

    input_program = program_name  # data에 있는 영화의 제목 입력

    program_index = programs[programs["original_title"] == input_program].index.values # input_program에 해당하는 index 값 가져오기
    similar_programs = similar_index[program_index, :100]    # 유사도 상위 100개 index 가져오기
    # 인덱스로 사용하기 위해서는 1차원으로 변형
    similar_programs_index = similar_programs.reshape(-1)   # similar_programs 1차원 변형
    # 해당하는 인덱스에 대한 영화 정보들을 가져온다.
    programs = programs.iloc[similar_programs_index]
    # 1000개 미만 평가를 받은 영화는 제외한다.
    programs = programs[programs["vote_count"] >= 1000]
    print(programs.head(10))  # 유사도 상위 10개 영화 가져오기


if __name__ == '__main__':
    program_name = "Rick and Morty"     # 영화 이름 지정
    start = time.time()  # 시작 시간 저장
    recommend(program_name)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간