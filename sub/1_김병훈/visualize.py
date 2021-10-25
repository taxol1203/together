import itertools
from collections import Counter
import folium
from pandas.core.indexes.datetimes import date_range
from parse import load_dataframes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


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
    # python itertools
    # Series를 1차원 이터레이터로 변환

    # 카테고리가 없는 경우 / 상위 카테고리를 추출합니다
    categories = filter(lambda c: c != "", categories)
    # python filter
    # 이터레이터를 필터 객체로 변환하며, 빈 값 제거

    categories_count = Counter(list(categories))
    best_categories = categories_count.most_common(n=n)
    # Counter.most_common
    # 가장 많이 등장하는 n개의 요소를 튜플로 이루어진 리스트 형태로 반환한다.

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
    r = stores.groupby("review_cnt").size().reset_index(name="count")
    r = r[r["review_cnt"] > 0]
    chart = sns.barplot(data=r, x="review_cnt", y="count")
    chart.set(yscale="log")
    plt.title("전체 음식점의 리뷰 개수 분포")
    plt.show()


def show_store_average_ratings_graph(dataframes):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    # stores Dataframe과 reviews Dataframe을 병합

    store_mean_score = (
        stores_reviews.groupby("store")["score"].mean().reset_index(name="mean_score")
    )
    # 평균 평점을 구하기 위해 score에 mean 메서드를 실행

    store_mean_score["mean_score"] = store_mean_score["mean_score"].round(decimals=1)
    # 평균 평점이 너무 파편화되어있어, 소수점 첫째자리를 기준으로 반올림하였음

    mean_score_count = (
        store_mean_score.groupby("mean_score").size().reset_index(name="count")
    )
    # 평균 평점 Column을 기준으로 그룹화
    # 같은 평균 평점을 갖고 있는 가게의 수를 세고, count라는 컬럼을 생성하여 저장

    chart = sns.scatterplot(x="mean_score", y="count", data=mean_score_count)
    chart.set(yscale="log")
    plt.title("각 음식점의 평균 평점")
    plt.show()


def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    users_reviews = pd.merge(
        dataframes["users"], dataframes["reviews"], left_on="id", right_on="user"
    )
    # users dataframe과 reviews dataframe을 병합

    users_review_cnt = (
        users_reviews.groupby(["user"]).size().reset_index(name="review_cnt")
    )
    # user column을 기준으로 그룹화
    # 동일한 유저 내에서

    grouped = users_review_cnt.groupby(["review_cnt"]).size().reset_index(name="count")
    chart = sns.scatterplot(data=grouped, x="review_cnt", y="count")
    chart.set(yscale="log")
    plt.title("전체 유저의 리뷰 개수")
    plt.show()
    # raise NotImplementedError


def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    users = dataframes["users"]
    # users = users[(0 < users["age"]) & (users["age"] < 100)]
    # 음수와 100살 기준으로 나이 필터링
    users = users[(19 < users["age"]) & (users["age"] < 40)]
    # 20 / 30대

    chart = sns.countplot(data=users, x="age", hue="gender")
    sns.move_legend(chart, "upper left")
    plt.title("전체 유저의 성별/나이대 분포")
    plt.xticks(fontsize=10, rotation="vertical")
    plt.show()


def show_stores_distribution_graph(dataframes):
    """
    Req. 1-3-5 각 음식점의 위치 분포를 지도에 나타냅니다.
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    stores = (
        stores_reviews.groupby(
            ["store", "store_name", "latitude", "longitude", "review_cnt"]
        )["score"]
        .mean()
        .reset_index(name="mean_score")
    )
    stores = stores.astype({"latitude": float, "longitude": float})
    stores["mean_score"] = stores["mean_score"].round(decimals=1)
    stores = stores[(stores["latitude"] > 0) & (stores["longitude"] > 0)]
    stores = (
        stores[(stores["review_cnt"] >= 10) & (stores["mean_score"] >= 4)]
        .reset_index()
        .drop(columns=["index"], axis=1)
    )

    lat = stores["latitude"].mean()
    long = stores["longitude"].mean()

    m = folium.Map([lat, long], zoom_start=8)
    for i in stores.index:
        s_lat = stores.loc[i, "latitude"]
        s_long = stores.loc[i, "longitude"]
        s_name = stores.loc[i, "store_name"]
        folium.Marker([s_lat, s_long], tooltip=s_name).add_to(m)
    m
    # raise NotImplementedError


def main():
    set_config()
    data = load_dataframes()
    # show_store_categories_graph(data)
    # show_store_review_distribution_graph(data)
    # show_store_average_ratings_graph(data)
    # show_user_review_distribution_graph(data)
    # show_user_age_gender_distribution_graph(data)
    show_stores_distribution_graph(data)


if __name__ == "__main__":
    main()
