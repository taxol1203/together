import itertools
from collections import Counter
from parse import load_dataframes
from analyze import sort_stores_by_score
from analyze import get_most_active_users
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import scipy
# import folium
# from folium import plugins


def set_config():
    # 폰트, 그래프 색상 설정
    font_list = fm.findSystemFonts(fontpaths=None, fontext="ttf")
    if any(["notosanscjk" in font.lower() for font in font_list]):
        plt.rcParams["font.family"] = "Noto Sans CJK JP"
    else:
        if not any(["malgun" in font.lower() for font in font_list]):
            raise Exception(
                "Font missing, please install Noto Sans CJK or Malgun Gothic. If you're using ubuntu, try `sudo apt install fonts-noto-cjk`"
            )

        plt.rcParams["font.family"] = "Malgun Gothic"

    sns.set_palette(sns.color_palette("Spectral"))
    plt.rc("xtick", labelsize=6)


def show_store_categories_graph(dataframes, n=100):
    """
    Tutorial: 전체 음식점의 상위 `n`개 카테고리 분포를 그래프로 나타냅니다.
    """

    stores = dataframes["stores"]

    # 모든 카테고리를 1차원 리스트에 저장합니다
    categories = stores.category.apply(lambda c: c.split("|"))
    categories = itertools.chain.from_iterable(categories)

    # 카테고리가 없는 경우 / 상위 카테고리를 추출합니다
    categories = filter(lambda c: c != "", categories)
    categories_count = Counter(list(categories))  
    best_categories = categories_count.most_common(n=n)

    df = pd.DataFrame(best_categories, columns=["category", "count"]).sort_values(
        by=["count"], ascending=False
    )

    # 그래프로 나타냅니다
    chart = sns.barplot(x="category", y="count", data=df)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("음식점 카테고리 분포")
    plt.show()


def show_store_review_distribution_graph(dataframes, n=100):
    """
    Req. 1-3-1 전체 음식점의 리뷰 개수 분포를 그래프로 나타냅니다. 
    """
    stores = dataframes["stores"]
    
    storesGroup = stores.groupby("review_cnt").size().reset_index(name="store_cnt")

    # 그래프로 나타냅니다
    chart = sns.barplot(x="review_cnt", y="store_cnt", data=storesGroup)

    # 리뷰가 0개인 데이터가 너무 많아 보기가 굉장히 불편함
    # y출 포멧팅 필요하다
    # yscale을 log로 변하게 함
    chart.set(yscale="log")
    plt.title("리뷰 개수 당 음식점 분포")
    plt.show()


def show_store_average_ratings_graph(dataframes, n=100):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """
    # sort_stores_by_score를 통해 음식점의 평균 평점을 받아오고 소숫점 1자리로 나타냄
    store_mean = sort_stores_by_score(dataframes, 10000, 10).round(1)
    
    scoreGroup = store_mean.groupby("score").size().reset_index(name = "mean_score_cnt")

    # y 축을 해당 평점을 갖는 음식점의 개수, x축을 평균 점수
    chart = sns.lineplot(x="score", y="mean_score_cnt", data=scoreGroup)
    plt.title("평균 평점 별 음식점의 분포")
    plt.xlabel('평균 평점')
    plt.ylabel('음식점의 개수')
    plt.show()


def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    userGroup = get_most_active_users(dataframes).head(100)
    
    reviewGroup = userGroup.groupby("reviews_cnt").size().reset_index(name = "count")

    chart = sns.barplot(x="reviews_cnt", y="count", data=reviewGroup)

    # 리뷰가 0개인 데이터가 너무 많아 보기가 굉장히 불편함
    # y출 포멧팅 필요하다
    # yscale을 log로 변하게 함
    chart.set(yscale="log")
    plt.title("리뷰 개수 당 유저 분포")
    plt.show()

def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    users = dataframes["users"]
    sns.countplot(x='age', hue='gender', data=users)
    plt.show()


def df_to_geojson(df):
    geojson = {'type': 'FeatureCollection', 'features': []}

    for _, row in df.iterrows():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": []},
            "properties": {}
        }
        feature['geometry']['coordinates'] = [row['longitude'], row['latitude']]
        feature['properties']['tel'] = row['tel']
        feature['properties']['address'] = row['address']
        feature['properties']['area'] = row['area']

        geojson['features'].append(feature)
    return geojson


def show_stores_distribution_graph(dataframes):
    """
    Req. 1-3-5 각 음식점의 위치 분포를 지도에 나타냅니다.
    """
    df = dataframes["stores"]
    # 리뷰가 10개 이상 달린
    df = df[df['review_cnt'] > 10]
    m = folium.Map(
        location=[35.8, 127.6], tiles="OpenStreetMap", zoom_start=8
    )
    geo_json = df_to_geojson(df)
    folium.GeoJson(geo_json, name="geojson").add_to(m)

    # 스크롤 기능
    plugins.MousePosition().add_to(m)
    # 전체화면 기능
    plugins.Fullscreen(
        position='topright',
        title='확장하기',
        title_cancel='나가기',
        force_separate_button=True
    ).add_to(m)

    m.save('map.html')




def main():
    set_config()
    data = load_dataframes()
    # show_store_categories_graph(data)
    # show_store_review_distribution_graph(data)
    # show_store_average_ratings_graph(data)
    
if __name__ == "__main__":
    main()
