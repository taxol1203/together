# %matplotlib inline -> 나중에 그래프화 할 때 사용하는 듯
import pandas as pd
import numpy as np
import json
import time
import os
import pickle


def recommend(rec_g1, rec_g2, rec_g3):
    try:
        md = pickle.load(open("program_genre_rec_df.pickle", "rb"))
    except (OSError, IOError) as e:
        dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/') + '/'  # 절대 경로로 설정 함 -> 나중에 서버에 올리면 문제가 되지 않을까?
        with open(dir + '../data/programs.json', 'r') as f:
            data = json.loads(f.read())

        md = pd.json_normalize(data)
        md = md.rename(columns={'pk': 'programId'})
        md = md.rename(columns={'fields.original_title': 'original_title'})
        md = md.rename(columns={'fields.overview': 'overview'})
        md = md.rename(columns={'fields.vote_count': 'vote_count'})
        md = md.rename(columns={'fields.vote_average': 'vote_average'})
        md = md.rename(columns={'fields.genre_ids': 'genres'})
        md = md.rename(columns={'fields.release_date': 'release_date'})
        md = md.rename(columns={'fields.popularity': 'popularity'})

        # errors='coerce' : 문자열이 속해있어서 오류가 날 경우 강제로 NaT으로 출력
        md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if not(pd.isnull(x)) else np.nan)
        pickle.dump(md, open("program_genre_rec_df.pickle", "wb"))

    # stack : 들어온 것 부터 쌓음
    s = md.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
    s.name = 'genre'
    gen_md = md.drop('genres', axis=1).join(s)

    # md = gen_md[gen_md['genre'] == program_genre]  # 여기에 장르를 기입한다
    # 여기에 입력받은 장르를 통해, 해당 받은 장르의 영화만 필터링 한다.
    md = gen_md[(gen_md['genre'] == rec_g1) | (gen_md['genre'] == rec_g2) | (gen_md['genre'] == rec_g3)]

    vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean() # 전체 report에 대한 평균 vote 수
    m = vote_counts.quantile(0.95) # 상위 5프로 영화

    qualified = md[(md['vote_count'] >= m) & (md['vote_count'].notnull()) & (md['vote_average'].notnull())][['programId', 'original_title', 'year', 'vote_count', 'vote_average', 'popularity', 'genre']]
    qualified['vote_count'] = qualified['vote_count'].astype('int')
    qualified['vote_average'] = qualified['vote_average'].astype('int')
    qualified.shape   # 288개의 영화가 포함될 자격이 있다.

    def weighted_rating(x) :
        v = x['vote_count']
        R = x['vote_average']
        return (v/(v+m) * R) + (m/(m+v) * C)

    qualified['wr'] = qualified.apply(weighted_rating, axis = 1)

    # wr기준으로 상위 250개의 영화만 골라냄
    qualified = qualified.sort_values('wr', ascending = False).head(250)
    print(qualified.head(15))
    # 추천 된 영화 제목들 반환
    qualified = qualified.head(15)
    result = []
    for program_id in qualified['programId']:
        result.append(program_id)
    return result

if __name__ == '__main__':
    program_genre = 35     # 영화 장르 지정
    start = time.time()  # 시작 시간 저장
    recommend(program_genre)
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
