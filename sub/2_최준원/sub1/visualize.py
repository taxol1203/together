import itertools
from collections import Counter
from parse import load_dataframes
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import folium
from folium import plugins


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
    # 음식점마다 리뷰를 보여주는게 아니라
    # stores = dataframes["stores"]
    # df = pd.DataFrame(stores, columns=["store_name", "review_cnt"]).sort_values(
    #     by=["review_cnt"], ascending=False
    # )
    # chart = sns.barplot(x="store_name", y="review_cnt", data=df.head(n))
    # chart.set_xticklabels(chart.get_xticklabels(), rotation=45)

    # 리뷰 개수에 따른 음식점의 분포도를 나타내는게 맞는 듯
    stores = dataframes["stores"]
    df = stores.groupby("review_cnt").size().reset_index(name="count")
    chart = sns.barplot(x="review_cnt", y="count", data=df)
    # y축이 너무 길어서 (리뷰가 0개인 데이터가 압도적으로 많아서) 데이터를 보기가 불편하다.
    # Then, how to set y axis range?
    # 축(axes, axis)의 포맷팅(lim, scale)의 편집이 필요
    # https://seaborn.pydata.org/examples/scatterplot_sizes.html?highlight=yscale
    # yscale을 log로 작은 수와 큰 수의 그래프 길이 차이를 줄인다.
    # linear: 선형스케일, log: 로그스케일, symlog: 시메트릭로그스케일 (음수영역), logit: 로짓스케일. 0과 1사이에 포함되는 데이터만으로 구성
    chart.set(yscale="log")
    plt.title("음식점 리뷰 개수 분포")
    plt.show()


def show_store_average_ratings_graph(dataframes, n=100):
    """
    Req. 1-3-2 각 음식점의 평균 평점을 그래프로 나타냅니다.
    """
    stores = dataframes["stores"]
    reviews = dataframes["reviews"]
    stores_reviews = pd.merge(
        stores, reviews, left_on="id", right_on="store"
    )
    # groupby를 해주지 않고 mean하니까 터진다. 주의할 것.
    # stores_reviews['score'].groupby([stores_reviews['store']])을 아래와 같이 축약할 수도 있다.
    scores_mean = stores_reviews.groupby(["store"])['score'].mean().reset_index(name="avg_score")
    # pandas.DataFrame.round
    scores_mean['avg_score'] = scores_mean['avg_score'].round(1)
    # 생성한 df의 x축을 평점, y축을 음식점의 수로 설정하기 위한 groupby
    df = scores_mean.groupby('avg_score').size().reset_index(name='count')
    chart = sns.barplot(x="avg_score", y="count", data=df)
    chart.set(yscale="log")
    plt.title("평균 평점 별 음식점의 분포")
    plt.show()


def show_user_review_distribution_graph(dataframes):
    """
    Req. 1-3-3 전체 유저의 리뷰 개수 분포를 그래프로 나타냅니다.
    """
    users = dataframes["users"]
    reviews = dataframes["reviews"]
    users_reviews = pd.merge(
        users, reviews, left_on="id", right_on="user"
    )
    # xaxis = 유저, yaxis = 리뷰 수
    reviews_per_user = users_reviews.groupby('user').size().reset_index(name='review_cnt')
    # xaxis = 리뷰 수, yaxis = 유저 수
    df = reviews_per_user.groupby('review_cnt').size().reset_index(name='users')
    chart = sns.barplot(x="review_cnt", y="users", data=df)
    chart.set(yscale="log")
    plt.title("리뷰 개수 별 유저의 분포")
    plt.show()


def show_user_age_gender_distribution_graph(dataframes):
    """
    Req. 1-3-4 전체 유저의 성별/나이대 분포를 그래프로 나타냅니다.
    """
    users = dataframes["users"]
    df = users.groupby(['age', 'gender']).size().reset_index(name='count')
    # 잘못된 나이 (음수, 150 이상) 제거
    # |, &를 쓰니까
    # ValueError: The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
    df = df[df['age'] > 0]
    df = df[df['age'] < 150]
    chart = sns.catplot(x="age", y="count", hue="gender", kind="bar", data=df)
    plt.title("전체 유저의 성별/나이대 분포")
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
    # show_user_review_distribution_graph(data)
    # show_user_age_gender_distribution_graph(data)
    show_stores_distribution_graph(data)


if __name__ == "__main__":
    main()
