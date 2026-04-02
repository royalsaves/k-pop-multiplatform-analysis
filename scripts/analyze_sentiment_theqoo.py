import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
from transformers import pipeline

# Load the sentiment data
def load_sentiment_data(file_path):
    return pd.read_csv(file_path)

# Analyze sentiment
def analyze_sentiment(data):
    from transformers import pipeline
    sentiment_analyzer = pipeline("sentiment-analysis", model="beomi/KcELECTRA-base-v2022")
    def get_label(text):
        result = sentiment_analyzer(str(text))[0]
        label = result['label']
        # LABEL_0: negative, LABEL_1: positive (임시 매핑)
        if label == 'LABEL_0':
            return 'negative'
        elif label == 'LABEL_1':
            return 'positive'
        else:
            return 'neutral'
    # 3번째 컬럼(제목) 기준 감정분석
    data['sentiment'] = data.iloc[:,2].apply(get_label)
    return data

# Save results to CSV
def save_results(df, output_path):
    # 날짜별로 긍/부정/중립 비율 집계
    summary = df.groupby('date')['sentiment'].value_counts(normalize=True).unstack(fill_value=0)
    # 컬럼명 표준화
    summary = summary.rename(columns={'POSITIVE': 'positive', 'NEGATIVE': 'negative', 'NEUTRAL': 'neutral'})
    for col in ['positive', 'neutral', 'negative']:
        if col not in summary.columns:
            summary[col] = 0.0
    summary = summary[['positive', 'neutral', 'negative']]
    summary.to_csv(output_path)

def load_env_from_file(env_path):
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    k, v = line.strip().split('=', 1)
                    os.environ[k] = v

# 날짜 필터링 함수
def is_in_comeback_period(date_str):
    try:
        date = datetime.strptime(date_str[:10], '%Y-%m-%d')
    except Exception:
        return False
    return datetime(2025,4,7) <= date <= datetime(2025,4,20)

def preprocess_theqoo_data(input_path, output_path):
    import re
    # 날짜 컬럼을 문자열로 읽도록 dtype 지정
    df = pd.read_csv(input_path, dtype={'날짜': str})
    # robust 날짜 변환 함수 (04.20, 4.14, 4.2, 25-04-20 등 모두 2025-04-20 포맷)
    def parse_date(date_str):
        s = str(date_str).strip()
        # YY-MM-DD → 2025-MM-DD로 보정 (25-04-19 → 2025-04-19)
        m = re.match(r'^(\d{2})-(\d{2})-(\d{2})$', s)
        if m:
            _, month, day = m.groups()
            return f'2025-{month}-{day}'
        # MM.DD, M.DD 등 → 2025-MM-DD
        m = re.match(r'^(\d{1,2})[.](\d{1,2})$', s)
        if m:
            month, day = m.groups()
            return f'2025-{int(month):02d}-{int(day):02d}'
        # 이미 2025-로 시작하면 그대로
        if s.startswith('2025-'):
            return s
        return ''
    df['date'] = df['날짜'].apply(parse_date)
    cols = ['date'] + [c for c in df.columns if c != 'date']
    df = df[cols]
    df['text'] = df['본문']
    df.to_csv(output_path, index=False)
    print(f"[전처리] {len(df)}건 저장: {output_path}")
    # date, 제목만 남긴 파일도 별도 저장
    df_simple = df[['date', '제목']]
    df_simple.to_csv('data/theqoo/theqoo_nct_all_filtered_simple.csv', index=False)
    print(f"[전처리] date, 제목만 저장: data/theqoo/theqoo_nct_all_filtered_simple.csv")

def analyze_sentiment_per_row(input_path, output_path):
    df = pd.read_csv(input_path)
    sentiment_analyzer = pipeline("sentiment-analysis", model="beomi/KcELECTRA-base-v2022")
    def get_label(text):
        result = sentiment_analyzer(str(text))[0]
        label = result['label']
        if label == 'LABEL_0':
            return 'negative'
        elif label == 'LABEL_1':
            return 'positive'
        else:
            return 'neutral'
    df['sentiment'] = df['제목'].apply(get_label)
    df.to_csv(output_path, index=False)
    print(f"[감정분석] {output_path} 저장 완료")

def analyze_emotion_per_row(input_path, output_path):
    import pandas as pd
    df = pd.read_csv(input_path)
    # 감정별 키워드 사전(업데이트)
    emotion_keywords = {
        'positive': [
            '귀여', '귀엽', '힐링', '뽀뽀', 'ㅋㅋ', '비상',
            '예쁘', '예뻐', '잘해', '잘했', '잘하', '좋아', '좋', '좋겠',
            '재미', '재밋', '재밌', '웃'
        ],
        'sadness': ['ㅠㅠ', 'ㅜㅜ', '슬프', '아쉽', '서운', '눈물'],
        'curious': ['?','궁금','질문'],
        # 실제 데이터에는 등장하지 않지만, 부정 감정 예시 키워드(향후 필요시 사용)
        'negative': ['별로', '실망', '최악', '망했다', '짜증', '화남', '싫다', '안좋', '실패', '불만', '못하', '안된다']
    }
    def get_emotion(text):
        text = str(text)
        for emotion, keywords in emotion_keywords.items():
            if any(kw in text for kw in keywords):
                return emotion
        return 'neutral'
    df['emotion'] = df['제목'].apply(get_emotion)
    df.to_csv(output_path, index=False)
    print(f"[감정분석] {output_path} 저장 완료")

def dual_emotion_analysis(sentiment_path, emotion_path, output_path):
    """
    두 감정분석 결과(긍/부정, 멀티클래스 emotion)를 결합하고, 의미상 일치 여부(match) 컬럼을 추가하여 저장
    """
    # 파일 로드
    df_sentiment = pd.read_csv(sentiment_path)
    df_emotion = pd.read_csv(emotion_path)
    # row 수 일치 보장
    assert len(df_sentiment) == len(df_emotion)
    # 결합
    df = df_sentiment.copy()
    df['emotion'] = df_emotion['emotion']
    # 긍/부정-감정 매핑
    positive_emotions = ['기쁨', '행복', '웃음', '설렘', '흥분', '감사', '사랑', '희망', '만족']
    negative_emotions = ['분노', '슬픔', '불안', '짜증', '실망', '두려움', '혐오', '질투', '후회', '걱정']
    # match 컬럼 생성
    def is_match(row):
        sent = row['sentiment']
        emo = row['emotion']
        if sent == 'positive' and emo in positive_emotions:
            return 'match'
        elif sent == 'negative' and emo in negative_emotions:
            return 'match'
        elif sent == 'neutral' and emo not in positive_emotions + negative_emotions:
            return 'match'
        else:
            return 'mismatch'
    df['match'] = df.apply(is_match, axis=1)
    df.to_csv(output_path, index=False)
    print(f"[듀얼 감정분석] {output_path} 저장 완료")

if __name__ == "__main__":
    import sys
    # 원본 대신 simple 파일을 입력으로 사용
    input_file = 'data/theqoo/theqoo_nct_all_filtered_simple_with_emotion.csv'
    output_file = 'data/theqoo/theqoo_nct_all_filtered_simple_with_emotion.csv'

    # 감정분석(키워드 기반, 최신 키워드 반영)
    analyze_emotion_per_row(
        input_file,
        output_file
    )
    print(f"[최종 감정분석 결과] {output_file} 만 남김")