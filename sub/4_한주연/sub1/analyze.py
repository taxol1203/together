from parse import load_dataframes
import pandas as pd
import shutil


def sort_stores_by_score(dataframes, n=20, min_reviews=30):
    """
    Req. 1-2-1 각 음식점의 평균 평점을 계산하여 높은 평점의 음식점 순으로 `n`개의 음식점을 정렬하여 리턴합니다
    -> 현재 음식점 별 평균 평점을 구하는 코드는 완성되어 있음
    우리가 해야할 것 : 평균 평점을 기준으로 음식점을 정렬하여 리턴
    
    Req. 1-2-2 리뷰 개수가 `min_reviews` 미만인 음식점은 제외합니다.
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    
    # 리뷰 개수가 `min_reviews` 미만인 음식점은 제외합니다.
    # store 컬럼을 기준으로 group by를한다. 그리고 store_name을 표시한다.
    # 이 이유는, 이후 mean()을 하였을 때 정수형 컬럼을 제외하고 다 생략되지만, 이름을 확인하기 위해 stor_name을 추가한다.
    scores_group = stores_reviews[stores_reviews['review_cnt'] >= min_reviews].groupby(["store", "store_name", "branch", "review_cnt"])
    
    # 평균 평점을 기준으로 음식점을 정렬하여 리턴
    scores = scores_group.mean().sort_values(by=['score'], axis=0, ascending=False) # 평균 구하기

    return scores.head(n=n).reset_index()


def get_most_reviewed_stores(dataframes, n=20):
    """
    Req. 1-2-3 가장 많은 리뷰를 받은 `n`개의 음식점을 정렬하여 리턴합니다
    """
    stores_reviews = pd.merge(
        dataframes["stores"], dataframes["reviews"], left_on="id", right_on="store"
    )
    reviews = stores_reviews.groupby(["store", "store_name", "branch", "review_cnt", "tel", "area"])
    reviews_mean = reviews.mean()   # groupby를 했으면, 연산은 꼭 해야한다.

    stores_sorted_by_reviews = reviews_mean.sort_values(by='review_cnt', ascending=False)
    return stores_sorted_by_reviews.head(n=n).reset_index()


def get_most_active_users(dataframes, n=20):
    """
    Req. 1-2-4 가장 많은 리뷰를 작성한 `n`명의 유저를 정렬하여 리턴합니다.
    """
     # user와 review를 병합
    users_reviews = pd.merge(
        dataframes["users"], dataframes["reviews"], left_on="id", right_on="user"
    )
    # 확인하고 싶은 컬럼을 넣고, size() 함수를 사용하면 몇 개의 데이터가 group으로 묶였는지 새로운 컬럼이 생성된다. dataFrameGroup의 경우, count()와 같다.
    # 이후 reset_index, rename을 사용해 원하는 컬럼명을 설정한 뒤 사용한다.
    users = users_reviews.groupby(["user", "gender", "age"]).size().reset_index(name='reviews_cnt')

    users_sorted_by_review_counts = users.sort_values(by='reviews_cnt', ascending=False)
    return users_sorted_by_review_counts.head(n=n).reset_index()


def main():
    data = load_dataframes() # DUMP_FILE = os.path.join(DATA_DIR, "dump.pkl")

    # 단순 출력 형식문
    term_w = shutil.get_terminal_size()[0] - 1
    separater = "-" * term_w

    stores_most_scored = sort_stores_by_score(data)

    print("[최고 평점 음식점]")
    print(f"{separater}\n")
    for i, store in stores_most_scored.iterrows():
        print(
            "{rank}위: {store}({score}점)".format(
                rank=i + 1, store=store.store_name, score=store.score
            )
        ) 
    print(f"\n{separater}\n\n")


if __name__ == "__main__":
    main()
