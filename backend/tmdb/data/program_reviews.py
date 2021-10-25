import json
import requests
from tmdb import URLMaker
from dotenv import load_dotenv
import pandas as pd

# Hide API KEY
# verbose: .env 파일 누락 등의 경고 메시지 출력 옵션
load_dotenv(verbose=True)
# TMDB_KEY = os.getenv('TMDB_KEY')        # "export TMDB_KEY=(발급 받은 api key)" 로 key를 환경 변수로 추가 해주어야 한다.
TMDB_KEY = 'ce028cad82d684aa4fb7bed674115688'
url = URLMaker(TMDB_KEY)


def create_program_review_data():
    count = 0

    # 영화 ID 리스트를 불러오기 위해, 이전에 만든 programs.json을 가져온다.
    with open('programs.json', 'r') as f:
        data = json.loads(f.read())
    df_nested_list = pd.json_normalize(data)
    
    print('-- 영화 리뷰 데이터 작업 시작 --')

    review_data = []
    # 각 영화마다 해당하는 리뷰를 가져온다.
    for program_id in df_nested_list['pk']:  
        review_url = url.get_program_review_url(program_id = program_id, page = 1)
        raw_data = requests.get(review_url)
        json_data = raw_data.json()
        total_review = json_data.get('total_results') # 총 리뷰 수를 가져온다.
        for page in range(1, total_review):
            review_url = url.get_program_review_url(program_id = program_id, page = page)
            raw_data = requests.get(review_url)
            json_data = raw_data.json()
            reviews = json_data.get('results')

            # 여러 리뷰 중, 리뷰 하나 씩을 가져온다.
            for review in reviews:
                # 리뷰 중, rating을 작성하지 않은 리뷰는 생략한다.
                if review['author_details']['rating'] == None:
                    review['author_details']['rating'] = 5

                tmp = {
                    'userId': review['author_details']['username'],
                    'programId': program_id,
                    'rating': review['author_details']['rating'],
                }
                # print(tmp)
                review_data.append(tmp)     # 리뷰를 담는다.
                count += 1  # 리뷰의 개수를 추가한다.
                if count % 100 == 0:
                    print(f'Currently, {count} have been saved.')

    # 모두 담긴 리뷰를 program_reviews.json으로 만든다.
    with open('program_reviews.json', 'w') as f:
        json.dump(review_data, f, indent=4)
    print(f'The total number of reviews is {count}')
    pass


if __name__ == '__main__':
    create_program_review_data()
