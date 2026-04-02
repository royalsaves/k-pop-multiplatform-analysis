# K-POP 멀티플랫폼 반응 분석

## 1. 프로젝트 개요
건국대학교 정보통신대학원 과제로 진행한 데이터 분석 프로젝트다.

주제는 특정 K-POP 그룹의 컴백 기간 전후 반응을 여러 플랫폼에서 같이 보는 것이었고, 이번 저장소에는 당시 사용한 수집 스크립트, 정제 데이터, 결과 그래프를 정리해 두었다.

분석 대상은 아래 세 축으로 잡았다.

- YouTube: 영상 업로드 메타데이터, 조회수, 댓글 수
- theqoo: 게시글 제목 기반 반응량과 감정 분류
- Google Trends: 기간 내 검색량 변화

## 2. 분석 범위
관측 기간은 2025-04-07부터 2025-04-20까지다.

이 기간을 기준으로 플랫폼별 데이터를 모으고, 일자 단위로 다시 맞춘 뒤 추세 그래프를 만들었다.

## 3. 저장소 구성
```text
.
├── data/
│   ├── theqoo/
│   ├── trends/
│   └── youtube/
├── result/
├── scripts/
├── run_data_script.py
└── requirements.txt
```

## 4. 디렉토리 설명
### 4.1 data
수집 후 정제한 CSV를 두는 경로다.

- `data/youtube`: YouTube 검색 결과 기반 메타데이터와 정제 결과
- `data/theqoo`: 게시글 제목과 감정 분류 결과
- `data/trends`: Google Trends 검색량 데이터

### 4.2 scripts
수집, 정제, 시각화 스크립트를 모아둔 경로다.

- [`scripts/youtube_data.py`](/Users/steve/myproject/konkuk/k-pop/scripts/youtube_data.py): YouTube Data API 기반 수집
- [`scripts/theqoo_data.py`](/Users/steve/myproject/konkuk/k-pop/scripts/theqoo_data.py): theqoo 게시글 수집
- [`scripts/google_trends.py`](/Users/steve/myproject/konkuk/k-pop/scripts/google_trends.py): Google Trends 수집
- [`scripts/analyze_sentiment_theqoo.py`](/Users/steve/myproject/konkuk/k-pop/scripts/analyze_sentiment_theqoo.py): 제목 기반 감정 분류
- [`scripts/create_graph.py`](/Users/steve/myproject/konkuk/k-pop/scripts/create_graph.py): 최종 그래프 생성

### 4.3 result
최종 보고용 그래프를 저장하는 경로다.

- `theqoo_daily_post.png`
- `youtube_video_views.png`
- `google_trends_nct.png`
- `emotion_overall_pie.png`
- `emotion_trends.png`
- `multiplatform_trend.png`

## 5. 처리 흐름
이번 과제는 아래 순서로 진행했다.

1. 플랫폼별 데이터 수집
2. 기간 필터링과 컬럼 정리
3. theqoo 게시글 제목 기준 감정 분류
4. 일자 단위 집계
5. 플랫폼별 추세와 정규화 그래프 생성

## 6. 실행 방법
### 6.1 의존성 설치
```bash
pip install -r requirements.txt
```

### 6.2 수집 스크립트 실행
YouTube 수집은 API 키가 필요하다. 루트에 `.secret_env`를 두고 아래 형식으로 설정한다.

```bash
cp .secret_env.example .secret_env
```

이후 스크립트를 직접 실행하면 된다.

```bash
python scripts/youtube_data.py "NCT WISH"
python scripts/theqoo_data.py
python scripts/google_trends.py
```

### 6.3 그래프 생성
```bash
python scripts/create_graph.py
```

## 7. 결과 파일
현재 저장소에는 정제된 데이터와 결과 그래프를 같이 남겨 두었다.

이 상태에서는 API 호출 없이도 결과 그래프를 다시 생성할 수 있다.

## 8. 정리 메모
이번 저장소로 남긴 범위는 아래와 같다.

- 과제에서 사용한 데이터 수집 코드
- 정제 후 CSV
- 감정 분류와 시각화 코드
- 결과 이미지

민감정보에 해당하는 API 키 파일은 추적 대상에서 제외했고, 공개 저장소에는 예시 파일만 두었다.
