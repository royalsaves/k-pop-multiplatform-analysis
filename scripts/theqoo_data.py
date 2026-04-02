import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from datetime import datetime

def load_env_from_file(env_path):
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v

def parse_theqoo_date(date_text, start_date, end_date):
    """더쿠 날짜 포맷을 robust하게 datetime으로 변환 (월.일은 end_date.year로 해석)"""
    now = datetime.now()
    try:
        # 1. 오늘 시간만: '19:51' → 오늘 날짜
        if len(date_text) == 5 and date_text.count(":") == 1:
            return datetime(now.year, now.month, now.day)
        # 2. 월.일: '04.07' → end_date.year 기준
        if len(date_text) == 5 and date_text.count(".") == 1:
            return datetime(end_date.year, int(date_text[:2]), int(date_text[3:]))
        # 3. 연.월.일(2자리): '24.04.07'
        if len(date_text) == 8 and date_text.count(".") == 2:
            return datetime.strptime(date_text, "%y.%m.%d")
        # 4. 연.월.일(4자리): '2024.04.07'
        if len(date_text) == 10 and date_text.count(".") == 2:
            return datetime.strptime(date_text, "%Y.%m.%d")
        # 5. 상대적 표현: '어제', '방금', 'n분 전' 등
        if any(x in date_text for x in ["어제", "방금", "전"]):
            return None  # 로그만 남기고 skip
    except Exception:
        return None
    return None

def collect_theqoo_data():
    mid = "nctwish"  # NCT WISH 카테고리만
    headers = {"User-Agent": "Mozilla/5.0"}
    base_url = "https://theqoo.net"
    results = []
    # 2주간 날짜 범위
    start_date = datetime(2025, 4, 7)
    end_date = datetime(2025, 4, 20)
    for page in range(1, 1000):  # 페이지를 충분히 넓게
        url = f"{base_url}/index.php?mid={mid}&page={page}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")
        except Exception as e:
            print(f"[페이지 요청 실패] {url} : {e}")
            continue
        rows = soup.select("tr:not(.notice)")
        print(f"[DEBUG] page {page} rows: {len(rows)}")
        last_post_date = None
        for row in rows:
            title_tag = row.select_one("td.title a[href^='/']")
            if not title_tag:
                continue
            href = title_tag.get("href")
            title = title_tag.text.strip()
            post_url = base_url + href
            date_text = "날짜없음"
            date_tag = row.select_one("td.time")
            if date_tag:
                date_text = date_tag.text.strip()
            print(f"[DEBUG] title: {title} | date: {date_text} | url: {post_url}")
            post_date = parse_theqoo_date(date_text, start_date, end_date)
            if post_date is None:
                print(f"[날짜 파싱 실패] {post_url} : {date_text}")
                continue
            last_post_date = post_date  # 마지막 게시글 날짜 갱신
            if start_date <= post_date <= end_date:
                # 본문은 상세페이지에서 추출
                try:
                    post_res = requests.get(post_url, headers=headers, timeout=10)
                    post_soup = BeautifulSoup(post_res.text, "html.parser")
                    content_tag = post_soup.select_one(".resContents_new")
                    content_text = content_tag.get_text(separator="\n").strip() if content_tag else "본문없음"
                except Exception as e:
                    print(f"[게시글 파싱 실패] {post_url} : {e}")
                    content_text = "본문없음"
                results.append({
                    "게시판": mid,
                    "제목": title,
                    "날짜": date_text,
                    "본문": content_text,
                    "URL": post_url
                })
                time.sleep(0.05)
        time.sleep(0.1)
        # 마지막 게시글 날짜가 start_date보다 이전이면 종료
        if last_post_date is not None and last_post_date < start_date:
            print(f"[INFO] 페이지 {page}의 마지막 게시글 날짜가 범위보다 이전({last_post_date.date()})이므로 크롤링 종료.")
            break
    save_results(results)

def save_results(results):
    print(f"[DEBUG] 크롤링 결과 수집된 게시글 수: {len(results)}")
    df = pd.DataFrame(results)
    save_path = os.path.join(os.path.dirname(__file__), '../data/theqoo/theqoo_nct_all_filtered.csv')
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    if df.empty:
        print(f"[경고] 저장할 데이터가 없습니다. 빈 CSV(헤더만) 저장: {save_path}")
        # 최소한의 헤더만 저장
        columns = ['게시판', '제목', '날짜', '본문', 'URL']
        pd.DataFrame(columns=columns).to_csv(save_path, index=False)
    else:
        df.to_csv(save_path, index=False)
        print(f"\n✅ NCT WISH 카테고리 2주간 게시글 {len(df)}개 수집 완료 → {save_path} 저장 완료")

if __name__ == "__main__":
    load_env_from_file(os.path.join(os.path.dirname(__file__), '..', '.secret_env'))
    collect_theqoo_data()