import os
import sys
import subprocess

print("==== K-POP 데이터 수집/분석 스크립트 선택 ====")
print("1. 유튜브 데이터 수집")
print("2. 더쿠 데이터 수집")
print("3. 구글 트렌드 데이터 수집")
choice = input("실행할 번호를 입력하세요 (1/2/3): ").strip()

if choice == "1":
    print("[유튜브 데이터 수집 스크립트 백그라운드 실행]")
    subprocess.Popen([sys.executable, "scripts/fetch_youtube_data.py", "NCT WISH"], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
elif choice == "2":
    print("[더쿠 데이터 수집 스크립트 백그라운드 실행]")
    subprocess.Popen([sys.executable, "scripts/fetch_theqoo_data.py"], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
elif choice == "3":
    print("[구글 트렌드 데이터 수집 스크립트 백그라운드 실행]")
    subprocess.Popen([sys.executable, "scripts/fetch_google_trends.py"], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
else:
    print("잘못된 입력입니다. 1, 2, 3 중에서 선택하세요.")
