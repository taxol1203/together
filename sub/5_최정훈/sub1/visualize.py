import itertools
from collections import Counter
from os import name

from pandas.core.frame import DataFrame
from pandas.core.reshape.pivot import pivot_table
from parse import load_dataframes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
import numpy as np
from scipy import sparse

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
    best_categories = categories_count.most_common(n=n) # 카테고리가 없는 것 중 가장 동일한 자료가 많은 것을 구함.
    df = pd.DataFrame(best_categories, columns=["category", "count"]).sort_values(
        by=["count"], ascending=False
    )

    # 그래프로 나타냅니다
    chart = sns.barplot(x="category", y="count", data=df)
    chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
    plt.title("음식점 카테고리 분포")
    plt.show()


def show_store_review_distribution_graph(dataframes):
    """
    Req. 1-3-1 전체 음식점의 리뷰 개수 분포를 그래프로 나타냅니다. 
    """
    stores = dataframes["stores"]
    # 리뷰 갯수를 1차원 리스트에 저장합니다.
    reviews_cnt = (
        stores.groupby("review_cnt").review_cnt.count().reset_index(name="count")
    )
    # print(reviews_cnt)
    chart = sns.barplot(x="review_cnt", y="count", data=reviews_cnt)
    # matplotlib.pylplot.yscale
    # value : linear, log, symlog, logit
    chart.set(yscale="log")
    plt.title("전체 음식점의 리뷰 개수 분포")
    plt.show()


def show_store_average_ratings_graph(dataframes):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """
    # 음식점과 리뷰 data merge
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    #store로 grouping 후 해당 store의 score(평점)의 평균을 mean_score colomn으로 만들고 reset_index
    store_mean_score = (
        stores_reviews.groupby("store").score.mean().reset_index(name="mean_score")
    )
    # store_maen_score에서 mean_score의 첫째 자리수에서 반올림(decimals=1)
    store_mean_score["mean_score"] = store_mean_score["mean_score"].round(decimals=1)
    # 리뷰 평점의 store의갯수를 count로 reset_index 
    mean_score_count = (
        store_mean_score.groupby("mean_score").store.count().reset_index(name="count")
    )
    chart = sns.barplot(x="mean_score", y="count", data=mean_score_count)
    chart.set(yscale="log")
    plt.title("각 음식점의 평균 평점")
    plt.show()


def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    # 유저와 리뷰 
    users_reviews = pd.merge(
        dataframes["users"], dataframes["reviews"], left_on="id", right_on="user"
    )
    users_review_cnt = (
        users_reviews.groupby(["user"]).user.count().reset_index(name="review_cnt")
    )
    grouped = (
        users_review_cnt.groupby(["review_cnt"]).review_cnt.count().reset_index(name="count")
    )
    chart = sns.barplot(x="review_cnt", y="count", data=grouped)
    chart.set(yscale="log")
    plt.title("전체 유저의 리뷰 개수")
    plt.show()


def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    users_reviews = pd.merge(
        dataframes["users"], dataframes["reviews"], left_on="id", right_on="user"
    )
    users_age_gender = (
        users_reviews.groupby(["gender", "user", "age"]).user.count().reset_index(name="user_age_gender_cnt")
    )
    # 범위를 벗어난 나이값 제거
    users_age_gender = users_age_gender[users_age_gender["age"] > 0]
    users_age_gender = users_age_gender[users_age_gender["age"] < 100] 
    
    # print(users_age_gender.head())
    chart = sns.countplot(x="age", hue="gender", data=users_age_gender)
    chart.set_yticklabels(chart.get_yticklabels(), rotation=100)
    plt.title("전체 유저의 성별/나이대")
    plt.show()

def show_stores_distribution_graph(dataframes):
    """
    Req. 1-3-5 각 음식점의 위치 분포를 지도에 나타냅니다.
    """
    # Folium 라이브러리
    # 지역, 리뷰수, 평점을 주어 나타내라
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"] , left_on="id", right_on="store"
    )

    # score가 기준이고 그 앞에 있는 groupby는 보여줄 것들
    store_place = stores_reviews.groupby(["store", "store_name", "review_cnt", "latitude", "longitude"])["score"].mean().reset_index(name="mean_score")
    store_place = store_place.astype({"latitude": float, "longitude": float})
    store_place["mean_score"] = store_place["mean_score"].round(decimals=1)
    store_place = (
        store_place[(store_place["review_cnt"] >= 10) & (store_place["mean_score"] >=4)].reset_index().drop(columns=["index"], axis=1)
    )   
    lat = store_place["latitude"].mean()
    lng = store_place["longitude"].mean()
    

    m = folium.Map([lat, lng], zoom_start=10)
    for i in store_place.index:
        n_lat = store_place.loc[i, "latitude"]
        n_lng = store_place.loc[i, "longitude"]
        n_name = store_place.loc[i, "store_name"]
        folium.Marker([n_lat, n_lng], tooltip = n_name).add_to(m)
        
    m.save('store.html')

def main():
    set_config()
    data = load_dataframes()
    # show_store_categories_graph(data)
    # show_store_review_distribution_graph(data)
    # show_store_average_ratings_graph(data)
    # show_user_review_distribution_graph(data)
    # show_user_age_gender_distribution_graph(data)
    # show_stores_distribution_graph(data)
    

if __name__ == "__main__":
    main()
