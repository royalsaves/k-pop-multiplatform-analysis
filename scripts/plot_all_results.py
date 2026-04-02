import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_youtube_data():
    # Load YouTube data
    video_counts = pd.read_csv('data/youtube/video_counts_by_day.csv')
    views = pd.read_csv('data/youtube/views_by_day.csv')
    comment_counts = pd.read_csv('data/youtube/comment_counts_by_day.csv')

    # Plot video counts
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=video_counts, x='date', y='count', label='Video Counts')
    plt.title('YouTube Video Counts by Day')
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('result/youtube_video_counts.png')
    plt.close()

    # Plot views
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=views, x='date', y='total_views', label='Total Views', color='orange')
    plt.title('YouTube Total Views by Day')
    plt.xlabel('Date')
    plt.ylabel('Total Views')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('result/youtube_total_views.png')
    plt.close()

    # Plot comment counts
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=comment_counts, x='date', y='comment_count', label='Comment Counts', color='green')
    plt.title('YouTube Comment Counts by Day')
    plt.xlabel('Date')
    plt.ylabel('Comment Count')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('result/youtube_comment_counts.png')
    plt.close()

def plot_theqoo_data():
    # Load Theqoo data
    sentiment = pd.read_csv('data/theqoo/sentiment_by_day.csv')

    # Plot sentiment
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=sentiment, x='date', y='sentiment_score', label='Sentiment Score', color='purple')
    plt.title('Theqoo Sentiment Score by Day')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('result/theqoo_sentiment_score.png')
    plt.close()

def plot_google_trends():
    # Load Google Trends data
    trends = pd.read_csv('data/trends/google_trends_data.csv')

    # Plot Google Trends
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=trends, x='date', y='trend_value', label='Google Trends', color='red')
    plt.title('Google Trends Data by Day')
    plt.xlabel('Date')
    plt.ylabel('Trend Value')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('result/google_trends.png')
    plt.close()

def load_env_from_file(env_path):
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v

if __name__ == "__main__":
    import sys
    load_env_from_file(os.path.join(os.path.dirname(__file__), '..', '.secret_env'))
    plot_youtube_data()
    plot_theqoo_data()
    plot_google_trends()