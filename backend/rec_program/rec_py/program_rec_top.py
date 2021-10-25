# %matplotlib inline -> 나중에 그래프화 할 때 사용하는 듯
import pandas as pd
import numpy as np
import json
import pickle
import os


def recommend():
    try:
        md = pickle.load(open("program_top_rec_df.pickle", "rb"))
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

        pickle.dump(md, open("program_top_rec_df.pickle", "wb"))
        
    # 다음 차례는 chart에 등록되기 위한 최소한의 vote 수인 m에 적절한 값을 결정하는 것이다. 우리는 95% 백분위 수를 우리의 컷오프로 사용합니다.
    # 즉, 영화가 차트에 포함되려면 목록에 있는 영화의 95% 이상보다 더 많은 표가 있어야합니다.

    # v : 영화의 vote 수
    # m : chart에 등록되기 위한 최소한의 vote 수
    # R : 영화 평점의 평균
    # C : 전체 report에 대한 평균 vote 수
    vote_counts = md[md['vote_count'].notnull()]['vote_count'].astype('int')
    vote_averages = md[md['vote_average'].notnull()]['vote_average'].astype('int')
    C = vote_averages.mean() # 전체 report에 대한 평균 vote 수
    C  # 평균적으로 6.1표씩 받음

        # chart에 등록되기 위한 최소한의 vote 수
    m = vote_counts.quantile(0.95) # 상위 5프로 영화

    # errors='coerce' : 문자열이 속해있어서 오류가 날 경우 강제로 NaT으로 출력
    md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if not(pd.isnull(x)) else np.nan)

    qualified = md[(md['vote_count'] >= m) & (md['vote_count'].notnull()) & (md['vote_average'].notnull())][['programId', 'original_title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
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
    qualified = qualified.head(15)
    result = []
    for program_id in qualified['programId']:
        result.append(program_id)
    return result