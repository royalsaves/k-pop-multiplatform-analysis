import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

theqoo = pd.read_csv('data/theqoo/theqoo_nct_all_filtered_simple_with_emotion.csv')
trends = pd.read_csv('data/trends/google_trends_data.csv')
youtube = pd.read_csv('data/youtube/video_counts_by_day_cleaned.csv')

theqoo['date'] = pd.to_datetime(theqoo['date']).dt.strftime('%Y-%m-%d')
trends['date'] = pd.to_datetime(trends['date']).dt.strftime('%Y-%m-%d')
youtube['date'] = pd.to_datetime(youtube['publishedAt']).dt.strftime('%Y-%m-%d')

# 더쿠 일별 게시글 수
theqoo_daily = theqoo.groupby('date').size()
plt.figure(figsize=(12,6))
theqoo_daily.plot(marker='o', color='#E53935')
plt.title('더쿠 NCT WISH 일별 게시글 수')
plt.xlabel('날짜')
plt.ylabel('게시글 수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('result/theqoo_daily_post.png')
plt.close()

# 유튜브 일별 조회수 합계
youtube_daily_views = youtube.groupby('date')['view_count'].sum()
plt.figure(figsize=(12,6))
youtube_daily_views.plot(marker='o', color='#43A047')
plt.title('유튜브 NCT WISH 영상 조회수 합계(일별)')
plt.xlabel('날짜')
plt.ylabel('조회수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('result/youtube_video_views.png')
plt.close()

# 구글 트렌드
plt.figure(figsize=(12,6))
sns.lineplot(data=trends, x='date', y='NCT', marker='o', color='#29B6F6')
plt.title('구글 트렌드: NCT 검색량')
plt.xlabel('날짜')
plt.ylabel('트렌드 점수')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('result/google_trends_nct.png')
plt.close()

# 더쿠 전체 감정 비율(파이차트)
emotion_counts = theqoo['emotion'].value_counts()
plt.figure(figsize=(6,6))
colors = ['#E53935', '#43A047', '#29B6F6', '#FFD600', '#8E24AA'][:len(emotion_counts)]
plt.pie(emotion_counts, labels=emotion_counts.index, autopct='%1.1f%%', colors=colors, startangle=90, counterclock=False)
plt.title('Emotion Overall (전체 감정 비율)')
plt.tight_layout()
plt.savefig('result/emotion_overall_pie.png')
plt.close()

# 더쿠 감정별 일별 변화(Emotion Trends)
emotion_trends = theqoo.groupby(['date', 'emotion']).size().unstack(fill_value=0)
plt.figure(figsize=(12,6))
emotion_trends.plot(ax=plt.gca(), marker='o')
plt.title('Emotion Trends (감정별 일별 변화)')
plt.xlabel('날짜')
plt.ylabel('게시글 수')
plt.xticks(rotation=45)
plt.legend(title='감정', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.savefig('result/emotion_trends.png')
plt.close()

# 멀티플랫폼 트렌드(더쿠/유튜브/구글트렌드) - y축 정규화
trend_df = pd.DataFrame()
trend_df['더쿠'] = theqoo.groupby('date').size()
trend_df['유튜브'] = youtube.groupby('date')['view_count'].sum()
trend_df['구글트렌드'] = trends.set_index('date')['NCT'].astype(float)
trend_df = trend_df.fillna(0)
for col in trend_df.columns:
    max_val = trend_df[col].max()
    if max_val > 0:
        trend_df[col] = trend_df[col] / max_val
plt.figure(figsize=(12,6))
trend_df.plot(ax=plt.gca(), marker='o', linewidth=2)
plt.title('멀티플랫폼 트렌드 (더쿠/유튜브/구글, 정규화)')
plt.xlabel('날짜')
plt.ylabel('정규화 지표 (0~1)')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
plt.tight_layout()
plt.savefig('result/multiplatform_trend.png')
plt.close()

print('그래프 생성 완료')
