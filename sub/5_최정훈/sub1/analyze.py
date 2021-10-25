from os import name
from parse import load_dataframes
import pandas as pd
import shutil


def sort_stores_by_score(dataframes, n=20, min_reviews=30):
    """
    Req. 1-2-1 각 음식점의 평균 평점을 계산하여 높은 평점의 음식점 순으로 `n`개의 음식점을 정렬하여 리턴합니다
    Req. 1-2-2 리뷰 개수가 `min_reviews` 미만인 음식점은 제외합니다.
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    # 리뷰 갯수 min_reviews 이상인 음식점
    scores_group = stores_reviews[stores_reviews["review_cnt"] >= min_reviews].groupby(["store", "store_name", "branch", "review_cnt"])
    # 각 음식점의 평균 평점 중 높은 평점의 음식점 순 정렬
    scores = scores_group.mean().sort_values(by='score', ascending=False)
    return scores.head(n=n).reset_index()


def get_most_reviewed_stores(dataframes, n=20):
    """
    Req. 1-2-3 가장 많은 리뷰를 받은 `n`개의 음식점을 정렬하여 리턴합니다
    """
    # review 순으로 store를 정렬하기 위해
    # store와 review 데이터 프레임을 병합한다.
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    # 모든 컬럼을 다 확인하려고, 모든 컬럼을 넣음
    scores_group = stores_reviews.groupby(
        [
            "store",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category",
            "review_cnt", # 평가 수
        ]
    )
    # 리뷰 순으로 정렬
    scores_group_sorted_by_rc = (
        scores_group.store.count()
        .reset_index(name="review_count")
        .sort_values(["review_count"], ascending=False)
    )
    # 상위 n개의 음식점을 반환
    return scores_group_sorted_by_rc.head(n=n).reset_index()


def get_most_active_users(dataframes, n=20):
    """
    Req. 1-2-4 가장 많은 리뷰를 작성한 `n`명의 유저를 정렬하여 리턴합니다.
    """
    users_reviews = pd.merge(
        dataframes["users"], dataframes["reviews"], left_on="id", right_on="user"
    )
    users_reviews_group = (users_reviews.groupby(["user", "gender", "age"]).user.count().reset_index(name="review_count"))
    users_reviews_sorted = users_reviews_group.sort_values(["review_count"], ascending=False)

    return users_reviews_sorted.head(n=n).reset_index()
    


def main():
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    stores_most_scored = sort_stores_by_score(data)
    reviews_most_scored = get_most_reviewed_stores(data)
    users_most_scored = get_most_active_users(data)


    print("[최고 평점 음식점]")
    print(f"{separater}\n")
    for i, store in stores_most_scored.iterrows():
        print(
            "{rank}위: {store}({score}점)".format(
                rank=i + 1, store=store.store_name, score=store.score
            )
        )
    print(f"\n{separater}\n\n")

    print("[리뷰가 많은 음식점]")
    print(f"{separater}\n")
    for i, store in reviews_most_scored.iterrows():
        print(
            "{rank}위 : {store}({review_count}개)".format(
                rank=i + 1, store=store.store_name, review_count=store.review_count
            )
        )
    print(f"\n{separater}\n\n")

    print("[리뷰를 많이 작성한 유저]")
    print(f"{separater}\n")
    for i, users in users_most_scored.iterrows():
        print(
            "{rank}위 : {user}({review_count}개)".format(
                rank=i + 1, user=users.user, review_count=users.review_count
            )
        )
    print(f"\n{separater}\n\n")





if __name__ == "__main__":
    main()
