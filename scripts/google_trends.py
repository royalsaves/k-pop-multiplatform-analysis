import os
import pandas as pd
from pytrends.request import TrendReq
from datetime import datetime
import time

def load_env_from_file(env_path):
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v

def collect_google_trends(keywords, timeframe='today 5-y', max_retries=5, wait_sec=60):
    pytrends = TrendReq(hl='en-US', tz=360)
    for attempt in range(1, max_retries+1):
        try:
            time.sleep(2)
            pytrends.build_payload(keywords, timeframe=timeframe)
            time.sleep(2)
            data = pytrends.interest_over_time()
            data.to_csv('data/trends/google_trends_data.csv', index=True)
            print("Google Trends data fetched and saved to data/trends/google_trends_data.csv")
            return True
        except Exception as e:
            print(f"[경고] 구글 트렌드 요청 실패 (시도 {attempt}/{max_retries}): {e}")
            if '429' in str(e) or 'TooManyRequests' in str(e):
                if attempt < max_retries:
                    print(f"[안내] 429 오류: {wait_sec}초 후 재시도합니다...")
                    time.sleep(wait_sec)
                else:
                    print("[오류] 최대 재시도 횟수 초과. 잠시 후 다시 시도하세요.")
                    return False
            else:
                print("[오류] 알 수 없는 예외. 즉시 종료.")
                return False
    return False

# 날짜 필터링 함수
def is_in_comeback_period(date_str):
    try:
        date = datetime.strptime(date_str[:10], '%Y-%m-%d')
    except Exception:
        return False
    return datetime(2025,4,7) <= date <= datetime(2025,4,20)

if __name__ == "__main__":
    import sys
    load_env_from_file(os.path.join(os.path.dirname(__file__), '..', '.secret_env'))
    keywords = ['NCT Wish', 'poppop']  # 두 키워드로 검색
    ok = collect_google_trends(keywords, timeframe='2025-04-01 2025-04-30')
    if ok:
        # 구글 트렌드 데이터도 2주간만 필터링
        df = pd.read_csv('data/trends/google_trends_data.csv')
        date_col = 'date' if 'date' in df.columns else df.columns[0]
        df = df[df[date_col].apply(is_in_comeback_period)]
        df.to_csv('data/trends/google_trends_data.csv', index=False)
    else:
        print("[실패] 구글 트렌드 데이터 수집에 실패했습니다. 나중에 다시 시도하세요.")