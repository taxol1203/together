import requests
import json


class URLMaker:
    url = 'https://api.themoviedb.org/3'

    def __init__(self, key):
        self.key = key

    def get_movie_genre_url(self):
        url = f'{self.url}/genre/movie/list?api_key={self.key}'
        return url

    def get_movie_url(self, category='movie', feature='popular', page='1'):
        url = f'{self.url}/{category}/{feature}'
        url += f'?api_key={self.key}&language=ko-KR&page={str(page)}'
        return url

    def get_program_genre_url(self):
        url = f'{self.url}/genre/tv/list?api_key={self.key}'
        return url

    def get_program_url(self, category='tv', feature='popular', page='1'):
        url = f'{self.url}/{category}/{feature}'
        url += f'?api_key={self.key}&language=ko-KR&page={str(page)}'
        return url

    def get_provider_url(self, program_id, provider):
        url = f'{self.url}/{provider}/{program_id}/watch/providers'
        url += f'?api_key={self.key}'
        return url

    def get_all_review_url(self, review_idx):
        url = f'{self.url}/review/{review_idx}?api_key={self.key}'
        return url

    def get_movie_review_url(self, movie_id, page='1'):
        url = f'{self.url}/movie/{movie_id}/reviews'
        url += f'?api_key={self.key}&language=ko-KR&page={str(page)}'
        return url

    def get_program_review_url(self, program_id, page='1'):
        url = f'{self.url}/tv/{program_id}/reviews'
        url += f'?api_key={self.key}&language=en-US&page={str(page)}'
        return url

    # def get_program_episode_group_url(self, program_id):
    #     url = f'{self.url}/tv/{program_id}/episode_groups'
    #     url += f'?api_key={self.key}&language=ko-KR'
    #     return url

    # def get_program_episode_group_details_url(self, episode_group_id):
    #     url = f'{self.url}/tv/episode_group/{episode_group_id}'
    #     url += f'?api_key={self.key}&language=ko-KR'
    #     return url
