import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False


def plot_youtube_daily_views():
    youtube = pd.read_csv('data/youtube/video_counts_by_day_cleaned.csv')
    youtube['date'] = pd.to_datetime(youtube['publishedAt']).dt.strftime('%Y-%m-%d')
    youtube_daily_views = youtube.groupby('date')['view_count'].sum().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=youtube_daily_views, x='date', y='view_count', marker='o', color='#43A047')
    plt.title('유튜브 일별 조회수 합계')
    plt.xlabel('날짜')
    plt.ylabel('조회수')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('result/youtube_video_views.png')
    plt.close()


def plot_theqoo_daily_posts():
    theqoo = pd.read_csv('data/theqoo/theqoo_nct_all_filtered_simple_with_emotion.csv')
    theqoo_daily = theqoo.groupby('date').size().reset_index(name='count')

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=theqoo_daily, x='date', y='count', marker='o', color='#E53935')
    plt.title('더쿠 일별 게시글 수')
    plt.xlabel('날짜')
    plt.ylabel('게시글 수')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('result/theqoo_daily_post.png')
    plt.close()


def plot_google_trends():
    trends = pd.read_csv('data/trends/google_trends_data.csv')
    value_column = 'NCT' if 'NCT' in trends.columns else trends.columns[1]

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=trends, x='date', y=value_column, marker='o', color='#29B6F6')
    plt.title('구글 트렌드 검색량')
    plt.xlabel('날짜')
    plt.ylabel('트렌드 점수')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('result/google_trends_nct.png')
    plt.close()

if __name__ == "__main__":
    plot_youtube_daily_views()
    plot_theqoo_daily_posts()
    plot_google_trends()
