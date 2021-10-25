import json
import os
import requests
from tmdb import URLMaker
from dotenv import load_dotenv

# Hide API KEY
# verbose: .env 파일 누락 등의 경고 메시지 출력 옵션
load_dotenv(verbose=True)
# TMDB_KEY = os.getenv('TMDB_KEY')
TMDB_KEY = 'ce028cad82d684aa4fb7bed674115688'

url = URLMaker(TMDB_KEY)
# https://image.tmdb.org/t/p/original

def create_program_genre_data():
    genre_url = url.get_program_genre_url()
    raw_data = requests.get(genre_url)
    json_data = raw_data.json()
    genres = json_data.get('genres')

    genre_data = []

    for genre in genres:
        tmp = {
            'model': 'programs.genre',
            'pk': genre['id'],
            'fields': {
                'name': genre['name']
            }
        }
        genre_data.append(tmp)

    with open('programs_genre.json', 'w', encoding='utf8') as f:
        json.dump(genre_data, f, indent=4)


def check_KR_provider(data):
    try:
        data.get('KR')
    except AttributeError:
        return None
    return data.get('KR')


def create_program_data():
    #with open('programs.json', 'r+', encoding='utf-8') as f:
    #    program_data = json.load(f)
    program_data = []
    count = 0
    print('-- TV 프로그램 데이터 작업 시작 --')

    for page in range(1, 500):
        raw_data = requests.get(url.get_program_url(page=page))
        json_data = raw_data.json()
        programs = json_data.get('results')

        for program in programs:
            fields = {}
            fields['poster_path'] = program.get('poster_path')
            fields['name'] = program.get('name')
            fields['original_title'] = program.get('original_name')
            fields['overview'] = program.get('overview')
            fields['popularity'] = program.get('popularity')
            fields['release_date'] = program.get('first_air_date')
            fields['genre_ids'] = program.get('genre_ids')
            fields['first_air_date'] = program.get('first_air_date')
            fields['vote_average'] = program.get('vote_average')
            fields['vote_count'] = program.get('vote_count')
            fields['origin_country'] = program.get('origin_country')
            fields['like_users'] = []

            program_id = program.get('id')
            provider_raw_data = requests.get(url.get_provider_url(program_id, 'tv'))
            provider_json_data = provider_raw_data.json()
            provider_results = provider_json_data.get('results')

            # 한국에서 볼 수 없는 컨텐츠라면 건너뛰기
            KR_provider = check_KR_provider(provider_results)
            if KR_provider is None:
                continue
            else:
                fields['provider'] = KR_provider

            # Program detail
            # 너무 많은 데이터이므로 개별 API 접속으로 빼도록 하자
            # detail_raw_data = requests.get(url.get_program_detail_url(program_id))
            # details = detail_raw_data.json()

            # fields['seasons'] = details.get('seasons')
            # fields['genres'] = details.get('genres')
            # fields['number_of_episodes'] = details.get('number_of_episodes')
            # fields['number_of_seasons'] = details.get('number_of_seasons')
            # fields['seasons'] = details.get('seasons')

            json_model = {
                'model': 'programs.program',
                'pk': program_id,
                'fields': fields,
            }
            program_data.append(json_model)
            count += 1
            if count % 100 == 0:
                print(f'Currently, {count} have been saved.')
            '''
            Episodes datas
            시즌 데이터만 넣어도 많기 때문에 우선 건너뛴다
            '''
    with open('programs.json', 'w', encoding='utf-8') as f:
        json.dump(program_data, f, indent=4)

    print('-- TV 프로그램 데이터 작업 완료 --')


if __name__ == '__main__':
    # create_program_genre_data()
    create_program_data()
