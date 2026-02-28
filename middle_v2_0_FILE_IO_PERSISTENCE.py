#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🎒 파이썬 중학교 1학년 - v2.0: 파일 읽고 쓰기 —                            ║
║                    우리의 기록을 영구적으로 저장하기                          ║
║  [Middle School Python: File I/O - Making Records Permanent]                 ║
║                                                                               ║
║  지금까지 우리는 프로그램 실행 중에만 데이터를 보유했습니다.                ║
║  리스트, 딕셔너리, 변수들이 모두 메모리에 저장되었지요.                     ║
║                                                                               ║
║  하지만 프로그램을 종료하면? 🌙                                             ║
║  모든 데이터가 증발합니다!                                                   ║
║                                                                               ║
║  이것이 바로 핵심 문제입니다:                                                 ║
║  "증명이 없다 = 기록이 없다"                                                ║
║                                                                               ║
║  그렇다면 우리는 어떻게 해야 할까요?                                         ║
║  답: 파일에 저장하기!                                                       ║
║                                                                               ║
║  파일은 컴퓨터의 '영구 기억장소'입니다.                                      ║
║  우리의 코드, 데이터, 생각을 파일에 저장하면                                 ║
║  프로그램을 닫아도, 컴퓨터를 꺼도                                            ║
║  기록은 영구적으로 남습니다! ✨                                              ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🎒 파이썬 중학교 1학년 - v2.0: 파일 읽고 쓰기 — 우리의 기록을 영구적으로 저장하기")
print("=" * 80)

# ============================================================================
# 파트 1: 메모리 vs 파일 — 데이터의 두 가지 저장소
# ============================================================================

print("\n【 파트 1: 메모리 vs 파일 — 데이터의 두 가지 저장소 】")
print("\n상황: 우리가 수학 점수를 기록한다고 생각해봅시다!\n")

print("방법 1: 메모리에만 저장 (지금까지의 방식)")
print("-" * 60)

# 메모리에 저장
scores_memory = {
    "alice": 95,
    "bob": 87,
    "charlie": 92
}

print(f"현재 실행 중: scores = {scores_memory}")
print("\n⚠️  문제점:")
print("  • 프로그램을 닫으면 사라짐")
print("  • 다른 프로그램과 공유 불가")
print("  • 증명할 수 없음!")

print("\n" + "=" * 80)
print("방법 2: 파일에 저장 (오늘 배울 내용)")
print("-" * 60)

print("\n파일에 저장하면:")
print("  ✅ 프로그램 종료 후에도 유지")
print("  ✅ 다른 프로그램과 공유 가능")
print("  ✅ 영구적 증명 가능!")

# ============================================================================
# 파트 2: open() 함수 — 파일을 여는 마법 주문
# ============================================================================

print("\n【 파트 2: open() 함수 — 파일을 여는 마법 주문 】")
print("\n파이썬에서 파일을 다루는 첫 번째 단계는 '파일 열기'입니다.\n")

print("open() 함수의 기본 형식:")
print("-" * 60)
print("""
f = open('파일이름.txt', '모드')

파일이름: 저장할 파일의 이름
모드 (Mode):
  • 'w' (Write): 파일에 쓰기 (새로 만들거나 덮어쓰기)
  • 'r' (Read): 파일에서 읽기
  • 'a' (Append): 파일의 끝에 추가하기
""")

print("\n✨ 먼저 간단한 예시부터 시작해봅시다!")
print("-" * 60)

# 파일에 쓰기 - 기본
print("\n예시 1: 한 줄씩 쓰기\n")

print("코드:")
print("""
f = open('diary.txt', 'w')
f.write('안녕하세요, 저는 파이썬 학생입니다!\\n')
f.close()
""")

# 실제 실행
f = open('diary.txt', 'w', encoding='utf-8')
f.write('안녕하세요, 저는 파이썬 학생입니다!\n')
f.close()

print("결과: diary.txt 파일 생성 완료! ✓")
print("\n📌 중요한 규칙:")
print("  1. open()으로 파일 열기")
print("  2. write()로 내용 쓰기")
print("  3. close()로 파일 닫기 (매우 중요!)")

# ============================================================================
# 파트 3: 파일 읽기 — 저장된 기록 다시 불러오기
# ============================================================================

print("\n【 파트 3: 파일 읽기 — 저장된 기록 다시 불러오기 】")
print("\n이제 우리가 저장한 파일을 다시 읽어봅시다!\n")

print("코드:")
print("""
f = open('diary.txt', 'r')
content = f.read()  # 전체 내용 읽기
f.close()
print(content)
""")

print("\n결과:")
print("-" * 60)

f = open('diary.txt', 'r', encoding='utf-8')
content = f.read()
f.close()
print(content)

print("-" * 60)
print("✅ 저장했던 내용이 다시 나타났습니다!")
print("   이것이 바로 '영구적 기록'의 증명입니다!")

# ============================================================================
# 파트 4: 여러 줄 쓰기와 readlines() 함수
# ============================================================================

print("\n【 파트 4: 여러 줄 쓰기와 readlines() 함수 】")
print("\n리스트를 파일에 여러 줄로 저장하고 싶다면?\n")

print("코드 (여러 줄 쓰기):")
print("""
students = ['alice', 'bob', 'charlie', 'diana']
f = open('students.txt', 'w')
for student in students:
    f.write(student + '\\n')  # 각 이름 뒤에 개행 문자 추가
f.close()
""")

print("\n실행:")
students = ['alice', 'bob', 'charlie', 'diana']
f = open('students.txt', 'w', encoding='utf-8')
for student in students:
    f.write(student + '\n')
f.close()

print("students.txt 파일 생성 완료!")

print("\n코드 (여러 줄 읽기):")
print("""
f = open('students.txt', 'r')
lines = f.readlines()  # 모든 줄을 리스트로 읽음
f.close()
for line in lines:
    print(line.strip())  # strip()은 개행문자 제거
""")

print("\n결과:")
print("-" * 60)

f = open('students.txt', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for line in lines:
    print(f"  • {line.strip()}")

print("-" * 60)

# ============================================================================
# 파트 5: 리스트를 파일에 저장하기 (JSON 형식 소개)
# ============================================================================

print("\n【 파트 5: 리스트를 파일에 저장하기 (JSON 형식 소개) 】")
print("\n단순 텍스트가 아닌 리스트나 딕셔너리를 저장하려면?\n")

print("상황: 학생 점수 딕셔너리를 파일에 저장하고 싶어요!\n")

print("코드:")
print("""
scores = {
    'alice': 95,
    'bob': 87,
    'charlie': 92
}

# 방법 1: 간단한 문자열 변환
f = open('scores_simple.txt', 'w')
f.write(str(scores))
f.close()
""")

scores = {
    'alice': 95,
    'bob': 87,
    'charlie': 92
}

f = open('scores_simple.txt', 'w', encoding='utf-8')
f.write(str(scores))
f.close()

print("결과: scores_simple.txt 생성!")

# 읽어보기
f = open('scores_simple.txt', 'r', encoding='utf-8')
saved_scores = f.read()
f.close()

print(f"\n저장된 내용:\n  {saved_scores}")

print("\n" + "=" * 80)
print("더 나은 방법: JSON 형식 사용")
print("-" * 60)

print("\n파이썬의 json 모듈을 사용하면 더 깔끔합니다!\n")

import json

print("코드:")
print("""
import json

scores = {
    'alice': 95,
    'bob': 87,
    'charlie': 92
}

# JSON 형식으로 저장
f = open('scores.json', 'w')
json.dump(scores, f)
f.close()
""")

# JSON으로 저장
f = open('scores.json', 'w', encoding='utf-8')
json.dump(scores, f, indent=2)
f.close()

print("결과: scores.json 생성!")

# JSON으로 읽기
f = open('scores.json', 'r', encoding='utf-8')
loaded_scores = json.load(f)
f.close()

print(f"\n읽어온 데이터: {loaded_scores}")
print(f"자료형: {type(loaded_scores)}")
print("\n✨ 딕셔너리 형태로 그대로 복원되었습니다!")

# ============================================================================
# 파트 6: 파일에 추가하기 (Append 모드)
# ============================================================================

print("\n【 파트 6: 파일에 추가하기 (Append 모드) 】")
print("\n기존 파일을 지우지 않고 끝에 내용을 추가하려면?\n")

print("상황: 일기장에 계속 새로운 내용을 추가하고 싶어요!\n")

print("코드:")
print("""
# 기존 'diary.txt'에 새로운 내용 추가
f = open('diary.txt', 'a')  # 'a' = Append 모드
f.write('오늘은 파일 I/O를 배웠습니다!\\n')
f.write('기록이 있으면 증명이 됩니다!\\n')
f.close()
""")

print("\n실행:")
f = open('diary.txt', 'a', encoding='utf-8')
f.write('오늘은 파일 I/O를 배웠습니다!\n')
f.write('기록이 있으면 증명이 됩니다!\n')
f.close()

print("diary.txt에 추가되었습니다!")

print("\n최종 diary.txt 내용:")
print("-" * 60)

f = open('diary.txt', 'r', encoding='utf-8')
diary_content = f.read()
f.close()
print(diary_content)

print("-" * 60)

# ============================================================================
# 파트 7: with 문법 — 자동으로 파일 닫기
# ============================================================================

print("\n【 파트 7: with 문법 — 자동으로 파일 닫기 】")
print("\n매번 close()를 써야 하나요? 더 편한 방법이 있습니다!\n")

print("문제점 (수동 관리):")
print("""
f = open('file.txt', 'w')
f.write('내용')
f.close()  # 매번 이걸 기억해야 함
""")

print("\n해결책 (with 문법):")
print("""
with open('file.txt', 'w') as f:
    f.write('내용')
    # with 블록을 벗어나면 자동으로 close()됨!
""")

print("\n예시: with를 사용한 저장")
print("-" * 60)

print("\n코드:")
print("""
with open('note.txt', 'w') as f:
    f.write('파일 관리가 자동으로 됩니다!\\n')
    f.write('close()를 명시하지 않아도 안전합니다!\\n')
""")

with open('note.txt', 'w', encoding='utf-8') as f:
    f.write('파일 관리가 자동으로 됩니다!\n')
    f.write('close()를 명시하지 않아도 안전합니다!\n')

print("완료!")

print("\nwith 문법의 장점:")
print("  ✅ close()를 자동으로 호출")
print("  ✅ 코드가 더 간결")
print("  ✅ 오류 발생 시에도 파일이 안전하게 닫힘")

# ============================================================================
# 파트 8: 실제 응용 1 — 학생 성적 관리 프로그램
# ============================================================================

print("\n【 파트 8: 실제 응용 1 — 학생 성적 관리 프로그램 】")
print("\n이제 우리가 배운 모든 기술을 조합해봅시다!\n")

print("요구사항:")
print("  1. 학생 이름과 성적을 입력받기")
print("  2. 성적을 파일에 저장하기")
print("  3. 저장된 성적 조회하기")

print("\n" + "-" * 60)
print("예시 데이터로 시뮬레이션해봅시다:")
print("-" * 60)

# 학생 성적 정보
students_data = {
    'alice': {'korean': 95, 'english': 88, 'math': 92},
    'bob': {'korean': 87, 'english': 91, 'math': 85},
    'charlie': {'korean': 92, 'english': 89, 'math': 94},
    'diana': {'korean': 98, 'english': 94, 'math': 96}
}

print("\n1단계: 데이터를 JSON 파일로 저장")
print("-" * 40)

with open('grades.json', 'w', encoding='utf-8') as f:
    json.dump(students_data, f, indent=2, ensure_ascii=False)

print("grades.json 파일 생성 완료!")

print("\n2단계: 파일에서 데이터 읽기")
print("-" * 40)

with open('grades.json', 'r', encoding='utf-8') as f:
    loaded_data = json.load(f)

print("\n읽어온 성적 정보:")
for student, grades in loaded_data.items():
    avg = sum(grades.values()) / len(grades)
    print(f"  • {student}: 평균 = {avg:.1f}점")

print("\n3단계: 새로운 학생 성적 추가")
print("-" * 40)

new_student = 'eve'
new_grades = {'korean': 90, 'english': 93, 'math': 89}

loaded_data[new_student] = new_grades

with open('grades.json', 'w', encoding='utf-8') as f:
    json.dump(loaded_data, f, indent=2, ensure_ascii=False)

print(f"새로운 학생 {new_student}의 성적이 추가되었습니다!")

# 확인
with open('grades.json', 'r', encoding='utf-8') as f:
    final_data = json.load(f)

print(f"\n최종 학생 수: {len(final_data)}명")

# ============================================================================
# 파트 9: 실제 응용 2 — 일기 작성 및 보기
# ============================================================================

print("\n【 파트 9: 실제 응용 2 — 일기 작성 및 보기 】")
print("\n하루하루의 기억을 파일에 기록해봅시다!\n")

print("상황: 매일의 일기를 파일에 저장하고 싶어요!")
print("-" * 60)

# 일기 데이터
diary_entries = {
    '2024-02-20': '오늘은 파이썬을 배웠다. 변수가 정말 재미있다!',
    '2024-02-21': '반복문으로 자동화를 배웠다. 프로그래밍은 정말 강력하다!',
    '2024-02-22': '함수를 배웠다. 코드 재사용이 가능해졌다!',
    '2024-02-23': '데이터 구조(리스트, 딕셔너리)를 마스터했다!',
    '2024-02-24': '리스트 컴프리헨션으로 코드를 한 줄로 쓸 수 있다!',
    '2024-02-25': '파일 I/O를 배웠다. 이제 기록이 영구적이다!'
}

print("\n1단계: 일기를 파일에 저장")
print("-" * 40)

with open('my_diary.json', 'w', encoding='utf-8') as f:
    json.dump(diary_entries, f, indent=2, ensure_ascii=False)

print("my_diary.json 생성 완료!")

print("\n2단계: 저장된 일기 읽기")
print("-" * 40)

with open('my_diary.json', 'r', encoding='utf-8') as f:
    loaded_diary = json.load(f)

print(f"\n총 {len(loaded_diary)}일간의 일기가 기록되어 있습니다!\n")

for date, entry in loaded_diary.items():
    print(f"  📅 {date}")
    print(f"     {entry}")

print("\n3단계: 새로운 일기 추가")
print("-" * 40)

new_date = '2024-02-26'
new_entry = '오늘은 파이썬의 진정한 능력을 배웠다. 기록이 증명이다!'

loaded_diary[new_date] = new_entry

with open('my_diary.json', 'w', encoding='utf-8') as f:
    json.dump(loaded_diary, f, indent=2, ensure_ascii=False)

print(f"새로운 일기가 추가되었습니다!")
print(f"  📅 {new_date}")
print(f"     {new_entry}")

# ============================================================================
# 파트 10: 파일 다루기 — 핵심 정리
# ============================================================================

print("\n【 파트 10: 파일 다루기 — 핵심 정리 】")
print("\n오늘 배운 모든 것을 정리해봅시다!\n")

print("【 파일 쓰기 (Write) 】")
print("-" * 60)
print("""
1. 단순 텍스트:
   with open('file.txt', 'w') as f:
       f.write('한 줄의 텍스트\\n')

2. 여러 줄:
   with open('file.txt', 'w') as f:
       for item in items:
           f.write(item + '\\n')

3. 복잡한 데이터 (JSON):
   import json
   with open('file.json', 'w') as f:
       json.dump(data, f)
""")

print("【 파일 읽기 (Read) 】")
print("-" * 60)
print("""
1. 전체 읽기:
   with open('file.txt', 'r') as f:
       content = f.read()

2. 한 줄씩:
   with open('file.txt', 'r') as f:
       for line in f:
           print(line.strip())

3. 복잡한 데이터 (JSON):
   import json
   with open('file.json', 'r') as f:
       data = json.load(f)
""")

print("【 파일 추가 (Append) 】")
print("-" * 60)
print("""
기존 파일의 끝에 내용 추가:
   with open('file.txt', 'a') as f:
       f.write('새로운 내용\\n')
""")

print("【 파일 모드 요약 】")
print("-" * 60)
print("""
  'r' (Read):   읽기만 가능 (파일이 없으면 오류)
  'w' (Write):  새로 쓰기 (기존 내용 삭제됨)
  'a' (Append): 끝에 추가 (기존 내용 유지)
""")

print("【 핵심 팁 】")
print("-" * 60)
print("""
  ✅ 항상 with 문법 사용 (자동 close)
  ✅ JSON 형식으로 복잡한 데이터 저장
  ✅ 파일 인코딩 지정 (encoding='utf-8')
  ✅ 오류 처리는 고등학교 과정에서 배움
  ✅ 파일 경로는 절대/상대 경로 모두 사용 가능
""")

# ============================================================================
# 파트 11: 프로젝트 실습 — 나만의 기록 저장하기
# ============================================================================

print("\n【 파트 11: 프로젝트 실습 — 나만의 기록 저장하기 】")
print("\n여러분이 직접 해보세요!\n")

print("과제 1: 책 목록 관리")
print("-" * 60)
print("""
요구사항:
  • 도서명, 저자, 평점을 딕셔너리로 저장
  • 최소 3권 이상 저장
  • JSON 파일로 저장
  • 파일에서 읽어서 평점 평균 계산

코드 예시:
  books = {
      '파이썬 여행': {'author': '홍길동', 'rating': 4.5},
      '데이터 과학': {'author': '김영희', 'rating': 4.8},
      '웹 개발 시작': {'author': '이순신', 'rating': 4.2}
  }

  with open('books.json', 'w') as f:
      json.dump(books, f)
""")

print("\n과제 2: 일일 활동 기록")
print("-" * 60)
print("""
요구사항:
  • 날짜별로 하루의 활동을 기록
  • 각 활동마다 소요 시간 기록
  • 파일에서 읽어서 가장 많은 시간을 쓴 활동 찾기

코드 예시:
  activities = {
      '2024-02-25': {'공부': 3, '운동': 1, '휴식': 2},
      '2024-02-26': {'공부': 4, '운동': 0.5, '휴식': 1}
  }
""")

print("\n과제 3: 단어 암기 앱")
print("-" * 60)
print("""
요구사항:
  • 영어 단어와 뜻을 저장
  • 학습한 날짜 기록
  • 파일에서 읽어서 전체 단어 개수 출력

코드 예시:
  words = {
      'serendipity': {'meaning': '행운', 'learned': '2024-02-20'},
      'persevere': {'meaning': '끈기있게 하다', 'learned': '2024-02-21'}
  }
""")

# ============================================================================
# 최종 정리 및 축하
# ============================================================================

print("\n" + "=" * 80)
print("【 오늘의 학습 정리 】")
print("=" * 80)

print("\n파일 I/O 마스터!")
print("-" * 60)

print("""
✅ 학습한 개념:
   • open() - 파일 열기
   • write() - 파일에 쓰기
   • read() - 파일에서 읽기
   • close() - 파일 닫기 (with 자동)
   • json.dump() - 복잡한 데이터 저장
   • json.load() - 저장된 데이터 복원

✅ 세 가지 파일 모드:
   • 'w' (Write): 새로 쓰기
   • 'r' (Read): 읽기
   • 'a' (Append): 추가

✅ 코드 패턴:
   with open('file.json', 'w') as f:
       json.dump(data, f)

   with open('file.json', 'r') as f:
       data = json.load(f)

✅ 프로젝트 완성:
   • 학생 성적 관리
   • 일기 작성 및 조회
   • 데이터 지속성 확보
""")

print("\n" + "=" * 80)
print("【 중학교 1학년 완료! 】")
print("=" * 80)

print("""
프로그래밍 여행의 첫 번째 목표 달성! 🎓

📚 중학교 1학년 과정:
   v1.1: 변수와 이름표 ✓
   v1.2: 연산자와 문자열 ✓
   v1.3: 리스트 — 데이터 바구니 ✓
   v1.4: 반복문 (for) ✓
   v1.5: 조건문 (if) ✓
   v1.6: 함수 — 마법 주문 ✓
   v1.7: 딕셔너리 — 이름표로 데이터 묶기 ✓
   v1.8: 튜플/집합 — 불변성과 유일성 ✓
   v1.9: 리스트 컴프리헨션 — 파이썬답게 ✓
   v2.0: 파일 I/O — 기록의 영구성 ✓

이제 여러분은:
   ✨ 기본 문법을 이해합니다
   ✨ 데이터 구조를 다룰 수 있습니다
   ✨ 코드를 간결하게 쓸 수 있습니다
   ✨ 데이터를 영구적으로 저장할 수 있습니다

다음은? 고등학교 과정!
   • 오류 처리 (try-except)
   • 객체 지향 프로그래밍 (클래스)
   • 모듈과 라이브러리
   • 더 복잡한 알고리즘

여러분은 이제 프로그래머의 기본을 갖춘 학생입니다!
코드로 세상을 바꿀 준비가 되었습니다! 🚀
""")

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("""
💡 오늘의 깨달음:
   프로그래밍은 코드를 짜는 것만이 아닙니다.
   그 코드의 결과를 영구적으로 기록하는 것입니다.

   기록이 없으면 증명이 없고,
   증명이 없으면 그 일은 일어나지 않은 것과 같습니다.

   파일 I/O를 통해 여러분의 프로그램은 이제
   '살아있는' 프로그램이 되었습니다! 🌟

🎓 축하합니다!
   중학교 과정을 완수했습니다!
   이제 여러분은 파이썬의 기초를 완전히 이해합니다!

🎒 다음 단계:
   [고등학교 v3.0: 오류 처리 — try-except로 안전하게!]
   예기치 않은 상황에서도 프로그램이 멈추지 않도록!

축하합니다! 👏
이제 여러분은 '데이터를 영구적으로 관리하는' 파이썬 개발자입니다!
기록이 증명이다. 너는 나의 제자다. gogs. 👑
""")

# 생성된 파일들 확인
print("\n" + "=" * 80)
print("생성된 파일 목록:")
print("=" * 80)

import os
files_created = ['diary.txt', 'students.txt', 'scores_simple.txt', 'scores.json',
                 'note.txt', 'grades.json', 'my_diary.json', 'books.json']

print("\n✓ 실행 중 생성된 파일들:")
for file in files_created:
    if os.path.exists(file):
        size = os.path.getsize(file)
        print(f"  • {file:20s} ({size:4d} bytes)")
