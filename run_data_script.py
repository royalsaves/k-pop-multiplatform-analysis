import os
import sys
import subprocess

print("==== K-POP 데이터 수집 스크립트 선택 ====")
print("1. 유튜브 데이터 수집")
print("2. 더쿠 데이터 수집")
print("3. 구글 트렌드 데이터 수집")
print("4. 그래프 생성")
choice = input("실행할 번호를 입력하세요 (1/2/3/4): ").strip()

if choice == "1":
    print("[유튜브 데이터 수집 실행]")
    subprocess.run([sys.executable, "scripts/youtube_data.py", "NCT WISH"], check=False)
elif choice == "2":
    print("[더쿠 데이터 수집 실행]")
    subprocess.run([sys.executable, "scripts/theqoo_data.py"], check=False)
elif choice == "3":
    print("[구글 트렌드 데이터 수집 실행]")
    subprocess.run([sys.executable, "scripts/google_trends.py"], check=False)
elif choice == "4":
    print("[그래프 생성 실행]")
    subprocess.run([sys.executable, "scripts/create_graph.py"], check=False)
else:
    print("잘못된 입력입니다. 1, 2, 3, 4 중에서 선택하세요.")
