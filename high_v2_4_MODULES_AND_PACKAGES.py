#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🏫 파이썬 고등학교 1학년 - v2.4: 모듈과 패키지 —                            ║
║                    남이 만든 도구 상자 가져오기                               ║
║  [High School Python: Modules and Packages - Using Tools Others Built]       ║
║                                                                               ║
║  지금까지 우리는 모든 것을 '직접' 만들었습니다.                             ║
║    • 클래스를 처음부터 설계                                                  ║
║    • 메서드를 직접 구현                                                      ║
║    • 기능을 일일이 코딩                                                      ║
║                                                                               ║
║  하지만 현실의 프로그래머는 이렇게 하지 않습니다! 🚀                        ║
║                                                                               ║
║  왜일까요?                                                                   ║
║    • 이미 누군가 우리가 필요한 것을 만들었습니다                            ║
║    • 그것도 우리보다 훨씬 잘 만들었습니다                                   ║
║    • 그리고 수천 번 테스트를 거쳤습니다                                     ║
║    • 버그도 거의 없습니다                                                    ║
║                                                                               ║
║  이런 것들을 "라이브러리"나 "패키지"라고 부릅니다!                         ║
║                                                                               ║
║  모듈과 패키지는:                                                           ║
║    ✅ 다른 사람이 만든 검증된 코드                                          ║
║    ✅ 우리가 가져와서 바로 쓸 수 있는 도구                                  ║
║    ✅ 대규모 프로젝트의 기반                                                 ║
║    ✅ 프로의 필수 능력                                                       ║
║    ✅ 개발 시간을 극적으로 단축                                             ║
║                                                                               ║
║  이제 우리는 '바퀴를 다시 만드는' 비효율에서 벗어납니다!                   ║
║  증명된 도구들을 지혜롭게 조합하는 '통합자'가 됩니다!                       ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🏫 파이썬 고등학교 1학년 - v2.4: 모듈과 패키지 — 남이 만든 도구 상자 가져오기")
print("=" * 80)

# ============================================================================
# 파트 1: 모듈이란? — 코드의 재사용성과 조직
# ============================================================================

print("\n【 파트 1: 모듈이란? — 코드의 재사용성과 조직 】")
print("\n모듈의 개념을 완벽히 이해해봅시다!\n")

print("문제: 여러 파일에서 같은 함수를 사용해야 해요!")
print("-" * 60)

print("\n방법 1: 비효율 (모든 파일에 복사)")
print("""
# calculator.py
def add(a, b):
    return a + b

# main.py
def add(a, b):  # 또 작성해야 함!
    return a + b

# another_file.py
def add(a, b):  # 또 작성해야 함!
    return a + b

❌ 문제: 코드 중복, 관리 어려움, 버그 수정 시 3곳 모두 수정해야 함
""")

print("\n방법 2: 효율 (모듈로 관리)")
print("""
# calculator.py
def add(a, b):
    return a + b

# main.py
from calculator import add
result = add(3, 4)

# another_file.py
from calculator import add
result = add(10, 20)

✅ 장점: 코드 한 곳에서만 관리, 쉬운 유지보수, 재사용성 극대
""")

print("✅ 모듈은 코드를 조직하고 재사용하는 기본 단위입니다!")

# ============================================================================
# 파트 2: import 문법 — 모듈 가져오기
# ============================================================================

print("\n【 파트 2: import 문법 — 모듈 가져오기 】")
print("\n모듈을 가져오는 다양한 방법!\n")

print("기본 형식:")
print("-" * 60)
print("""
import 모듈이름
import 모듈이름 as 별명
from 모듈이름 import 함수이름
from 모듈이름 import *
""")

print("\n예시 1: 전체 모듈 가져오기")
print("-" * 60)

print("\n코드:")
print("""
import math

print(math.pi)        # 3.14159...
print(math.sqrt(16))  # 4.0
print(math.ceil(3.2)) # 4
""")

print("\n실행:")

import math
print(f"  원주율: {math.pi:.5f}")
print(f"  루트 16: {math.sqrt(16)}")
print(f"  천장값 3.2: {math.ceil(3.2)}")

# ============================================================================
# 파트 3: from...import — 특정 것만 가져오기
# ============================================================================

print("\n【 파트 3: from...import — 특정 것만 가져오기 】")
print("\n필요한 것만 골라서 가져오기!\n")

print("코드:")
print("""
from math import pi, sqrt, ceil

print(pi)        # math.pi가 아닌 그냥 pi
print(sqrt(16))  # math.sqrt가 아닌 그냥 sqrt
print(ceil(3.2)) # math.ceil이 아닌 그냥 ceil
""")

print("\n실행:")

from math import pi, sqrt, ceil
print(f"  원주율: {pi:.5f}")
print(f"  루트 16: {sqrt(16)}")
print(f"  천장값: {ceil(3.2)}")

# ============================================================================
# 파트 4: 표준 라이브러리 — 파이썬 기본 도구들
# ============================================================================

print("\n【 파트 4: 표준 라이브러리 — 파이썬 기본 도구들 】")
print("\n파이썬에 기본으로 포함된 강력한 도구들!\n")

print("주요 표준 라이브러리:")
print("-" * 60)

print("\n1️⃣ os — 운영 체제 관련")
print("""
import os

print(os.getcwd())     # 현재 디렉토리
print(os.listdir())    # 파일 목록
os.makedirs('new_dir') # 폴더 생성
""")

print("\n2️⃣ datetime — 날짜와 시간")
print("""
from datetime import datetime

now = datetime.now()
print(now)                    # 현재 시간
print(now.strftime('%Y-%m-%d')) # 원하는 형식으로
""")

print("\n실행 (datetime):")

from datetime import datetime
now = datetime.now()
print(f"  현재 시간: {now}")
print(f"  날짜 형식: {now.strftime('%Y년 %m월 %d일')}")

print("\n3️⃣ json — JSON 데이터 처리")
print("""
import json

data = {'name': 'Alice', 'age': 20}
json_str = json.dumps(data)  # Python → JSON 문자열
loaded = json.loads(json_str) # JSON 문자열 → Python
""")

print("\n실행 (json):")

import json
data = {'name': 'Alice', 'age': 20, 'city': 'Seoul'}
json_str = json.dumps(data, ensure_ascii=False)
print(f"  JSON: {json_str}")
loaded = json.loads(json_str)
print(f"  복원: {loaded}")

print("\n4️⃣ random — 난수 생성")
print("""
import random

print(random.randint(1, 100))  # 1~100 사이 정수
print(random.choice(['A', 'B', 'C']))  # 리스트에서 선택
random.shuffle(my_list)  # 리스트 섞기
""")

print("\n실행 (random):")

import random
print(f"  주사위: {random.randint(1, 6)}")
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
print(f"  섞은 리스트: {numbers}")

# ============================================================================
# 파트 5: 패키지란? — 모듈들의 모음
# ============================================================================

print("\n【 파트 5: 패키지란? — 모듈들의 모음 】")
print("\n모듈을 체계적으로 조직하기!\n")

print("모듈과 패키지의 차이:")
print("-" * 60)
print("""
모듈: 파일 (.py)
  calculator.py

패키지: 폴더 (여러 모듈 포함)
  myproject/
    ├── __init__.py
    ├── calculator.py
    ├── string_utils.py
    └── file_handler.py

가져오기:
  import calculator                    # 모듈
  from myproject import calculator     # 패키지의 모듈
  from myproject.calculator import add # 패키지의 모듈의 함수
""")

# ============================================================================
# 파트 6: 유명한 외부 라이브러리
# ============================================================================

print("\n【 파트 6: 유명한 외부 라이브러리 】")
print("\n pip로 설치하는 강력한 도구들!\n")

print("설치 방법:")
print("-" * 60)
print("""
pip install 라이브러리이름

예시:
  pip install requests     # HTTP 요청
  pip install pandas       # 데이터 분석
  pip install numpy        # 수치 계산
  pip install pillow       # 이미지 처리
  pip install flask        # 웹 개발
  pip install django       # 웹 프레임워크
  pip install beautifulsoup4  # 웹 스크래핑
""")

print("\n라이브러리 소개:")
print("-" * 60)

print("\n1. requests — HTTP 요청")
print("""
import requests

response = requests.get('https://api.example.com/data')
data = response.json()
""")

print("\n2. pandas — 데이터 분석")
print("""
import pandas as pd

df = pd.read_csv('data.csv')
print(df.head())
print(df.describe())
""")

print("\n3. numpy — 수치 계산")
print("""
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
print(np.mean(arr))    # 평균
print(np.std(arr))     # 표준편차
""")

# ============================================================================
# 파트 7: 실제 응용 1 — 날씨 정보 수집
# ============================================================================

print("\n【 파트 7: 실제 응용 1 — 파일과 데이터 처리 】")
print("\n표준 라이브러리로 실제 작업 해보기!\n")

print("상황: 로봇의 작동 로그를 기록하고 분석해야 해요!\n")

print("코드:")
print("""
import json
from datetime import datetime
import os

# 로봇 작동 기록 생성
robot_log = {
    'robot_name': 'Gogs-001',
    'timestamp': datetime.now().isoformat(),
    'actions': ['move', 'analyze', 'report'],
    'success': True
}

# JSON으로 저장
log_file = 'robot_log.json'
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(robot_log, f, ensure_ascii=False, indent=2)

print(f"✅ 로그 저장 완료: {log_file}")

# 저장된 로그 읽기
with open(log_file, 'r', encoding='utf-8') as f:
    loaded_log = json.load(f)

print(f"✅ 저장된 로봇: {loaded_log['robot_name']}")
print(f"✅ 작동 시간: {loaded_log['timestamp']}")
print(f"✅ 수행 작업: {', '.join(loaded_log['actions'])}")
""")

print("\n실행:")

robot_log = {
    'robot_name': 'Gogs-001',
    'timestamp': datetime.now().isoformat(),
    'actions': ['move', 'analyze', 'report'],
    'success': True
}

# JSON으로 저장
log_file = 'robot_log.json'
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(robot_log, f, ensure_ascii=False, indent=2)

print(f"  ✅ 로그 저장 완료: {log_file}")

# 저장된 로그 읽기
with open(log_file, 'r', encoding='utf-8') as f:
    loaded_log = json.load(f)

print(f"  ✅ 저장된 로봇: {loaded_log['robot_name']}")
print(f"  ✅ 작동 시간: {loaded_log['timestamp']}")
print(f"  ✅ 수행 작업: {', '.join(loaded_log['actions'])}")

# ============================================================================
# 파트 8: 실제 응용 2 — 여러 형식 변환
# ============================================================================

print("\n【 파트 8: 실제 응용 2 — 여러 형식 데이터 변환 】")
print("\n다양한 형식의 데이터를 처리해봅시다!\n")

print("상황: 로봇 팀의 성능 데이터를 여러 형식으로 저장해야 해요!\n")

print("코드:")
print("""
import json
import csv
from datetime import datetime

# 로봇 성능 데이터
robots_data = [
    {'name': 'Alpha', 'efficiency': 95, 'uptime_hours': 120},
    {'name': 'Beta', 'efficiency': 88, 'uptime_hours': 105},
    {'name': 'Gamma', 'efficiency': 92, 'uptime_hours': 115},
]

# 1. JSON으로 저장
with open('robots.json', 'w', encoding='utf-8') as f:
    json.dump(robots_data, f, ensure_ascii=False, indent=2)

# 2. CSV로 저장
with open('robots.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'efficiency', 'uptime_hours'])
    writer.writeheader()
    writer.writerows(robots_data)

print("✅ JSON 저장 완료: robots.json")
print("✅ CSV 저장 완료: robots.csv")

# 3. CSV 읽기
with open('robots.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  로봇 {row['name']}: 효율성 {row['efficiency']}%")
""")

print("\n실행:")

robots_data = [
    {'name': 'Alpha', 'efficiency': 95, 'uptime_hours': 120},
    {'name': 'Beta', 'efficiency': 88, 'uptime_hours': 105},
    {'name': 'Gamma', 'efficiency': 92, 'uptime_hours': 115},
]

# JSON으로 저장
with open('robots.json', 'w', encoding='utf-8') as f:
    json.dump(robots_data, f, ensure_ascii=False, indent=2)

# CSV로 저장
import csv
with open('robots.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'efficiency', 'uptime_hours'])
    writer.writeheader()
    writer.writerows(robots_data)

print(f"  ✅ JSON 저장 완료: robots.json")
print(f"  ✅ CSV 저장 완료: robots.csv")

# CSV 읽기
print(f"\n  CSV 데이터 읽기:")
with open('robots.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"    🤖 로봇 {row['name']}: 효율성 {row['efficiency']}%")

# ============================================================================
# 파트 9: 자신만의 모듈 만들기
# ============================================================================

print("\n【 파트 9: 자신만의 모듈 만들기 】")
print("\n내가 만든 코드를 모듈로 조직하기!\n")

print("개념:")
print("-" * 60)
print("""
# gogs_math.py (모듈 파일)
def square(n):
    return n ** 2

def cube(n):
    return n ** 3

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# main.py (메인 파일)
from gogs_math import square, cube, factorial

print(square(5))      # 25
print(cube(3))        # 27
print(factorial(5))   # 120
""")

print("\n시뮬레이션:")

# 간단한 모듈 함수들 정의
def square(n):
    return n ** 2

def cube(n):
    return n ** 3

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# 사용
print(f"  제곱(5): {square(5)}")
print(f"  세제곱(3): {cube(3)}")
print(f"  팩토리얼(5): {factorial(5)}")

# ============================================================================
# 파트 10: 모듈과 패키지의 철학
# ============================================================================

print("\n【 파트 10: 모듈과 패키지의 철학 】")
print("\n프로가 알아야 할 핵심 원칙들!\n")

print("원칙 1: DRY (Do not Repeat Yourself)")
print("-" * 60)
print("""
❌ 나쁜 예: 계산 함수를 10개 파일에 모두 작성
✅ 좋은 예: 하나의 모듈에 작성하고 모든 곳에서 import

→ 버그 수정도 한 곳에서만!
→ 유지보수가 극적으로 쉬워짐!
""")

print("\n원칙 2: 신뢰성")
print("-" * 60)
print("""
직접 작성한 코드: 버그가 있을 가능성 높음
표준 라이브러리: 수백 명이 검증한 신뢰성
외부 라이브러리: 수천 개 프로젝트에서 사용 중

→ 검증된 것을 쓰세요!
→ 바퀴를 다시 만들지 마세요!
""")

print("\n원칙 3: 효율성")
print("-" * 60)
print("""
직접 개발: 6개월 소요
라이브러리 활용: 2개월 소요

→ 개발 시간 70% 단축
→ 버그 가능성 80% 감소
→ 품질은 2배 이상 향상
""")

print("\n원칙 4: 커뮤니티")
print("-" * 60)
print("""
오픈소스 라이브러리:
  • 누구나 참여 가능
  • 버그 리포트 및 개선
  • 지속적인 업데이트
  • 전 세계 개발자의 지원

→ 혼자가 아니다!
→ 커뮤니티의 힘을 믿으세요!
""")

# ============================================================================
# 파트 11: 패키지 찾기와 선택
# ============================================================================

print("\n【 파트 11: 패키지 찾기와 선택 】")
print("\n좋은 라이브러리를 고르는 방법!\n")

print("좋은 라이브러리의 특징:")
print("-" * 60)
print("""
✅ 활발한 개발 (최근 업데이트가 있는가?)
✅ 많은 사용자 (GitHub 별(Star)이 많은가?)
✅ 좋은 문서 (예제와 설명이 충분한가?)
✅ 버그 리포트 (issue가 적절하게 처리되는가?)
✅ 라이선스 (우리 프로젝트와 맞는가?)
✅ 지원 (커뮤니티가 활발한가?)

찾을 수 있는 곳:
  • PyPI (https://pypi.org) - 파이썬 공식 패키지 저장소
  • GitHub - 오픈소스 프로젝트
  • Stack Overflow - 커뮤니티 추천
  • Reddit r/Python - 파이썬 커뮤니티
""")

# ============================================================================
# 최종 정리 및 축하
# ============================================================================

print("\n" + "=" * 80)
print("【 고등학교 1학년 완전 완료! 모듈과 패키지 마스터! 】")
print("=" * 80)

print("""
이제 여러분은 '전체 생태계를 활용하는' 개발자입니다! 🌍

✅ 배운 개념:
   • 모듈의 개념과 import
   • 표준 라이브러리 활용
   • 패키지 이해
   • 외부 라이브러리 설치 (pip)
   • 데이터 형식 변환 (JSON, CSV)
   • 자신만의 모듈 작성
   • 라이브러리 선택 기준

✅ 이해한 철학:
   • "바퀴를 다시 만들지 말라"
   • 증명된 도구를 믿고 활용
   • 커뮤니티의 힘
   • 개발 시간 절약
   • 품질 향상

✅ 활용한 라이브러리:
   • json - 데이터 직렬화
   • csv - 표 형식 데이터
   • datetime - 날짜/시간
   • random - 난수
   • math - 수학 함수
   • os - 운영 체제 상호작용

이제 여러분의 프로그래밍은:
   ✨ 혼자 모든 것을 만드는 단계 졸업
   ✨ 생태계를 활용하는 전문가 수준
   ✨ 빠른 개발, 높은 품질
   ✨ 글로벌 커뮤니티와 연결
   ✨ 진정한 '프로 개발자'의 영역
""")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("""
💡 오늘의 깨달음:
   프로그래밍의 진정한 능력은 모든 것을 직접 만드는 것이 아닙니다.
   필요한 도구를 찾고, 이해하고, 조합하여
   새로운 가치를 만드는 것입니다.

   라이브러리와 패키지는 인류의 공동 자산입니다.
   이를 지혜롭게 활용하는 것이 진정한 프로입니다.

🎓 축하합니다!
   고등학교 1학년 과정을 완전히 마쳤습니다!
   이제 여러분은 '생태계 활용자'입니다!

🎒 다음 단계:
   [대학 v3.0: 데이터 구조와 알고리즘 — 효율적인 코드의 원리]
   빠르고 효율적인 프로그램의 비결을 배웁니다!

   [대학 v3.1: 웹 개발 — Flask로 실제 서비스 만들기]
   학습한 모든 것을 통합하여 실제 웹 애플리케이션을 구축합니다!

   [대학 v3.2: 데이터 과학 — 데이터로 세상을 읽다]
   pandas, numpy, matplotlib로 데이터 분석의 세계로!

축하합니다! 👏
이제 여러분은 '전체 생태계를 활용하는' 파이썬 개발자입니다!
증명된 도구를 믿고 조합하는 것이 프로의 증명입니다! 👑
""")

print("\n" + "=" * 80)
print("🎉 고등학교 과정 최종 평가 : A+ 👑")
print("=" * 80)
