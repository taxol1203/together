import numpy as np 
import pandas as pd
import json
import time


def recommend(program_name):
    # -------- Load Dataset -----------

    # program json을 dataframe으로 만들기
    with open('data/programs.json', 'r') as f:
        data = json.loads(f.read())
    df_nested_list = pd.json_normalize(data)

    # 사용하는 column만 추출
    meta = df_nested_list[["pk", "fields.original_title", "fields.genre_ids"]]

    # id 컬럼 이름을 programId로 변경
    meta = meta.rename(columns={'pk':'programId'})
    meta = meta.rename(columns={'fields.original_title':'original_title'})
    # meta = meta.rename(columns={'fields.original_language':'original_language'})
    meta = meta.rename(columns={'fields.genre_ids':'genres'})

    # meta = meta[meta['original_language'] == 'en'] # 영어로만 되어있는 리뷰 가져옴

    # 유저 rating 파일 불러옴
    with open('data/program_reviews.json', 'r') as f:
        data = json.loads(f.read())
    ratings = pd.json_normalize(data)

    # ratings.head()

    # ratings.describe() # ratings 테이블의 기본 정보들을 알려준다. 개수, 평균, 최소, 등등

    # ------- Refine Dataset -----------

    # to_numeric으로 String인 데이터를 int로 바꾼다
    meta.programId = pd.to_numeric(meta.programId, errors='coerce')
    ratings.programId = pd.to_numeric(ratings.programId, errors='coerce')

    # meta.head()

    # ------------ Merge Meta and Ratings -----------
    # 유저 데이터와 영화 데이터를 movidId를 기준으로 merge 한다.
    data = pd.merge(ratings, meta, on='programId', how='inner')

    # data.head()

    # Pivot Table
    # Pivot table로 만들어 준다.
    # userId와 original_title를 기준으로 만들어준다.
    matrix = data.pivot_table(index='userId', columns='original_title', values='rating')

    # matrix.head(20)

    # ----------- 상관 관계 정하기 ----------
    # 피어슨 상관관계 ( Pearson Correlation )

    GENRE_WEIGHT = 0.001 # 같을 장르일 시, 더하는 가중치 값

    def pearsonR(s1, s2):
        s1_c = s1 - s1.mean()
        s2_c = s2 - s2.mean()
        return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

    def recommend_program(input_program, matrix, n, similar_genre=True):
        input_genres = meta[meta['original_title'] == input_program]['genres'].iloc(0)[0]

        result = []
        for title in matrix.columns:
            if title == input_program:
                continue

            # rating comparison
            cor = pearsonR(matrix[input_program], matrix[title])

            # genre comparison
            temp_genres = []
            if similar_genre and len(input_genres) > 0:
                temp_genres = meta[meta['original_title'] == title]['genres'].iloc(0)[0]

                same_count = np.sum(np.isin(input_genres, temp_genres))
                cor += (GENRE_WEIGHT * same_count)

            if np.isnan(cor):
                continue
            else:
                result.append((title, '{:.100f}'.format(cor), temp_genres))

        result.sort(key=lambda r: r[1], reverse=True)

        return result[:n]

    # Prediction
    recommend_result = recommend_program(program_name, matrix, 10, similar_genre=True)
    result = pd.DataFrame(recommend_result, columns=['Title', 'Correlation', 'Genre'])

    print(result)


if __name__ == '__main__':
    program_name = "The Walking Dead"     # 영화 이름 지정
    start = time.time()  # 시작 시간 저장
    recommend(program_name)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간