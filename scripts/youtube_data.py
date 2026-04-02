import pandas as pd
import requests
import os

def collect_youtube_data(api_key, query, start_date, end_date):
    base_url = "https://www.googleapis.com/youtube/v3"
    published_after = f"{start_date}T00:00:00Z"
    published_before = f"{end_date}T23:59:59Z"
    all_video_info = []
    next_page_token = None
    while True:
        video_url = (
            f"{base_url}/search?key={api_key}&q={query}&part=id,snippet&order=date&maxResults=50"
            f"&publishedAfter={published_after}&publishedBefore={published_before}"
        )
        if next_page_token:
            video_url += f"&pageToken={next_page_token}"
        video_response = requests.get(video_url).json()
        if 'items' not in video_response:
            print(f"[오류] YouTube API 응답에 'items'가 없습니다. 응답 내용: {video_response}")
            break
        # video_id, title, publishedAt 추출
        for item in video_response['items']:
            if (
                'videoId' in item['id'] and
                'snippet' in item and
                'title' in item['snippet'] and
                'publishedAt' in item['snippet']
            ):
                all_video_info.append({
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'publishedAt': item['snippet']['publishedAt']
                })
        next_page_token = video_response.get('nextPageToken')
        if not next_page_token:
            break
    if not all_video_info:
        print("[오류] videoId, title, publishedAt을 찾을 수 없습니다. 쿼리 조건을 확인하세요.")
        return []
    video_ids = [v['video_id'] for v in all_video_info]
    video_titles = {v['video_id']: v['title'] for v in all_video_info}
    video_dates = {v['video_id']: v['publishedAt'] for v in all_video_info}
    # Fetch video statistics (50개씩 나눠서 요청)
    video_data = []
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        stats_url = f"{base_url}/videos?key={api_key}&id={','.join(batch_ids)}&part=statistics"
        stats_response = requests.get(stats_url).json()
        if 'items' not in stats_response:
            continue
        for item in stats_response['items']:
            vid = item['id']
            video_data.append({
                'publishedAt': video_dates.get(vid, ''),
                'view_count': item['statistics'].get('viewCount', 0),
                'comment_count': item['statistics'].get('commentCount', 0),
                'title': video_titles.get(vid, ''),
                'video_id': vid
            })
    return video_data

def save_to_csv(data, filename):
    if not data:
        print(f"[경고] 저장할 데이터가 없습니다: {filename}")
        return
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # 원하는 컬럼 순서로 저장
    df = pd.DataFrame(data)
    columns = ['publishedAt', 'view_count', 'comment_count', 'title', 'video_id']
    df = df[columns]
    df.to_csv(filename, index=False)

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
    API_KEY = os.environ.get("YOUTUBE_API_KEY") or "YOUR_API_KEY"
    if API_KEY == "YOUR_API_KEY":
        print("[오류] API_KEY가 설정되지 않았습니다. .secret_env 파일을 확인하세요.")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("[오류] 검색어(q)를 인자로 입력하세요. 예시: python youtube_data.py NCT WISH")
        sys.exit(1)
    query = ' '.join(sys.argv[1:])
    # 컴백 전후 1주일(2025-04-07 ~ 2025-04-20)만 추출
    start_date = "2025-04-07"
    end_date = "2025-04-20"
    youtube_data = collect_youtube_data(API_KEY, query, start_date, end_date)
    save_to_csv(youtube_data, os.path.join('data', 'youtube', 'video_counts_by_day.csv'))