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

    scores = stores_reviews[stores_reviews['review_cnt'] >= min_reviews].groupby(["store", "store_name", "branch", "review_cnt"])
    scores_mean = scores.mean()

    sorted_by_scores = scores_mean.sort_values(by='score', ascending=False)
    return sorted_by_scores.head(n=n).reset_index()


def get_most_reviewed_stores(dataframes, n=20):
    """
    Req. 1-2-3 가장 많은 리뷰를 받은 `n`개의 음식점을 정렬하여 리턴합니다
    """

    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )

    reviews = stores_reviews.groupby(["store", "store_name", "branch", "review_cnt", "tel", "area"])
    reviews_mean = reviews.mean()

    stores_sorted_by_reviews = reviews_mean.sort_values(by="reviews_cnt", ascending=False)
    return stores_sorted_by_reviews.head(n=n).reset_index()


def get_most_active_users(dataframes, n=20):
    """
    Req. 1-2-4 가장 많은 리뷰를 작성한 `n`명의 유저를 정렬하여 리턴합니다.
    """

    users_reviews = pd.merge(
        dataframes["users"], dataframes["reviews"], left_on="id", right_on="user"
    )

    users = users_reviews.groupby(["user", "gender", "age"]).user.size().reset_index(name="reviews_cnt")

    users_sorted_by_review_cnt = users.sort_values(by="reviews_cnt", ascending=False)
    return users_sorted_by_review_cnt

def main():
    data = load_dataframes()

    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    stores_most_scored = sort_stores_by_score(data)

    print("[최고 평점 음식점]")
    for i, store in stores_most_scored.iterrows():
        print(
            "{rank}위: {store}({score}점)".format(
                rank=i + 1, store=store.store_name, score=store.score
            )
        )
    print(f"{separater}\n\n")


if __name__ == "__main__":
    main()
