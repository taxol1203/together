import json
import os
import requests
from tmdb import URLMaker
from dotenv import load_dotenv
import time

# Hide API KEY
# verbose: .env 파일 누락 등의 경고 메시지 출력 옵션
load_dotenv(verbose=True)
# TMDB_KEY = os.getenv('TMDB_KEY')        # "export TMDB_KEY=(발급 받은 api key)" 로 key를 환경 변수로 추가 해주어야 한다.

TMDB_KEY = 'ce028cad82d684aa4fb7bed674115688'

url = URLMaker(TMDB_KEY)

def create_movie_genre_data():
    genre_url = url.get_movie_genre_url()
    raw_data = requests.get(genre_url)
    json_data = raw_data.json()
    genres = json_data.get('genres')

    genre_data = []

    for genre in genres:
        tmp = {
            'model': 'movies.genre',
            'pk': genre['id'],
            'fields': {
                'name': genre['name']
            }
        }
        genre_data.append(tmp)

    with open('movies_genre.json', 'w') as f:
        json.dump(genre_data, f, indent=4)


def check_KR_provider(data):
    try:
        data.get('KR')
    except AttributeError:
        return None
    return data.get('KR')

def create_movie_data():
    #with open('movies.json', 'r+') as f:
    #    movie_data = json.load(f)
    count = 0 # 영화 개수를 출력하기 위한 변수
    movie_data = []
    print('-- 영화 데이터 작업 시작 --')

    for page in range(0, 500):
        raw_data = requests.get(url.get_movie_url(page=page))
        json_data = raw_data.json()
        movies = json_data.get('results')

        # if(count > 5700):
        #    print(f'Currently, {count} have been saved.')
        #    break
        
        if movies is None:
            print(f"find error point is : {count}")
            continue

        for movie in movies:
            fields = {}
            fields['poster_path'] = movie.get('poster_path')
            fields['title'] = movie.get('title')
            fields['original_title'] = movie.get('original_title')
            fields['original_language'] = movie.get('original_language')
            fields['overview'] = movie.get('overview')
            fields['adult'] = movie.get('adult')
            fields['popularity'] = movie.get('popularity')
            fields['release_date'] = movie.get('release_date')
            fields['genre_ids'] = movie.get('genre_ids')
            fields['vote_average'] = movie.get('vote_average')
            fields['vote_count'] = movie.get('vote_count')
            fields['like_users'] = []

            movie_id = movie.get('id')
            provider_raw_data = requests.get(url.get_provider_url(movie_id, 'movie'))
            provider_json_data = provider_raw_data.json()
            provider_results = provider_json_data.get('results')

            # 한국에서 볼 수 없는 컨텐츠라면 건너뛰기
            KR_provider = check_KR_provider(provider_results)
            if KR_provider is None:
                continue 
            else:
                fields['provider'] = KR_provider

            json_model = {
                'model': 'movies.movie',
                'pk': movie_id,
                'fields': fields,
            }
            movie_data.append(json_model)
            count += 1
            if(count % 100 == 0):
                print(f'Currently, {count} have been saved.')
    
    # movies.json에 저장
    with open('movies_kr.json', 'w') as f:
        json.dump(movie_data, f, indent=4)
    print(f'Total number of movies is {count}')
    print('-- 영화 데이터 작업 완료 --')


if __name__ == '__main__':
    start = time.time()  # 시작 시간 저장
    create_movie_genre_data()
    create_movie_data()
    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
