#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🎒 파이썬 중학교 1학년 - v1.8: 튜플(Tuple)과 집합(Set) —                   ║
║                       변하지 않는 기록과 중복 없는 모음                       ║
║  [Middle School Python: Tuples and Sets - Immutability & Uniqueness]         ║
║                                                                               ║
║  지금까지 배운 리스트는 매우 자유로웠습니다.                                ║
║  추가하고, 삭제하고, 수정할 수 있었죠.                                      ║
║                                                                               ║
║  하지만 생각해보세요:                                                        ║
║  "한 번 정한 규칙은 절대 바뀌면 안 된다"는 요구사항이 있다면?             ║
║  "중복된 데이터는 자동으로 제거되어야 한다"는 필요가 있다면?              ║
║                                                                               ║
║  그래서 파이썬은 두 가지 새로운 데이터 타입을 제공합니다:                 ║
║                                                                               ║
║  1️⃣ 튜플(Tuple): "한 번 정하면 절대 바뀌지 않는" 데이터                   ║
║     예: (2026, 2, 24) - 날짜는 바뀔 수 없습니다!                           ║
║                                                                               ║
║  2️⃣ 집합(Set): "중복이 없는" 모음                                          ║
║     예: {1, 2, 3} - 중복된 숫자는 자동 제거됩니다!                         ║
║                                                                               ║
║  리스트 < 튜플 < 불변 > 집합 < 유일성                                      ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🎒 파이썬 중학교 1학년 - v1.8: 튜플(Tuple)과 집합(Set)")
print("=" * 80)

# ============================================================================
# 파트 1: 튜플의 필요성 - 변하지 않는 데이터
# ============================================================================

print("\n【 파트 1: 튜플(Tuple) - 변하지 않는 기록 】")
print("\n상황: 우리는 '2026년 2월 24일'이라는 날짜를 저장했어요.\n")

print("방법 1: 리스트로 저장 (문제 있음!)")
date_list = [2026, 2, 24]
print(f"date_list = {date_list}")
print("\n문제점: 누군가가 실수로 월을 13으로 바꿀 수 있어요!")
date_list[1] = 13
print(f"date_list[1] = 13으로 변경됨: {date_list}")
print("→ 날짜가 잘못되었어요! 😱\n")

print("방법 2: 튜플로 저장 (안전함!)")
date_tuple = (2026, 2, 24)
print(f"date_tuple = {date_tuple}")
print("\n특징: 한 번 만들면 절대 바뀌지 않아요!")
print("→ 튜플은 '불변(Immutable)'입니다!")

# ============================================================================
# 파트 2: 튜플의 기본 구조
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 튜플 만들고 사용하기 】")
print("=" * 80)

print("\n튜플을 만드는 방법:\n")
print("tuple_name = (항목1, 항목2, 항목3)")
print("또는")
print("tuple_name = 항목1, 항목2, 항목3  # 괄호 생략 가능\n")

print("예시 1: 학생 정보 (변하지 않는 데이터)\n")

student_info = ("Alice", 25, "프로그래머")
print(f"student_info = {student_info}")
print(f"이름: student_info[0] = {student_info[0]}")
print(f"나이: student_info[1] = {student_info[1]}")
print(f"직업: student_info[2] = {student_info[2]}\n")

print("예시 2: 좌표 (GPS 위치)\n")

location = (37.7749, -122.4194)  # 샌프란시스코 좌표
print(f"location = {location}")
print(f"위도: {location[0]}")
print(f"경도: {location[1]}\n")

print("【 리스트와의 차이점 】")
print("  리스트: data_list[0] = 100  ✅ 수정 가능")
print("  튜플:  data_tuple[0] = 100  ❌ 에러! 수정 불가!")

# ============================================================================
# 파트 3: 튜플의 특성
# ============================================================================

print("\n" + "-" * 80)
print("파트 3: 튜플의 특성 — 불변성(Immutability)")
print("-" * 80)

print("\n시도 1: 튜플 요소 수정하기\n")

coordinates = (10, 20, 30)
print(f"coordinates = {coordinates}")
print("\n코드: coordinates[0] = 100")

try:
    coordinates[0] = 100
except TypeError as e:
    print(f"에러 발생: {e}")
    print("→ 튜플은 수정할 수 없습니다!\n")

print("시도 2: 튜플에 요소 추가하기\n")

print("코드: coordinates.append(40)")

try:
    coordinates.append(40)
except AttributeError as e:
    print(f"에러 발생: 튜플은 append 메서드가 없습니다")
    print("→ 튜플은 추가할 수 없습니다!\n")

print("시도 3: 튜플 요소 삭제하기\n")

print("코드: del coordinates[0]")

try:
    del coordinates[0]
except TypeError as e:
    print(f"에러 발생: {e}")
    print("→ 튜플은 삭제할 수 없습니다!\n")

print("【 튜플이 '불변'이라는 의미 】")
print("  ✅ 접근: 요소를 읽을 수 있음")
print("  ✅ 인덱싱: list[0]처럼 사용 가능")
print("  ✅ 슬라이싱: list[0:2]처럼 사용 가능")
print("  ❌ 수정: 요소를 바꿀 수 없음")
print("  ❌ 추가: 요소를 더할 수 없음")
print("  ❌ 삭제: 요소를 지울 수 없음")

# ============================================================================
# 파트 4: 튜플의 유용한 메서드
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 4: 튜플의 메서드 】")
print("=" * 80)

print("\n튜플도 리스트처럼 유용한 메서드를 가져요!\n")

numbers_tuple = (1, 2, 3, 2, 1, 2, 3)
print(f"numbers_tuple = {numbers_tuple}\n")

print("【 count(): 특정 요소의 개수 】")
count_2 = numbers_tuple.count(2)
print(f"2가 몇 개? numbers_tuple.count(2) = {count_2}\n")

print("【 index(): 특정 요소의 위치 】")
index_3 = numbers_tuple.index(3)
print(f"3은 어디? numbers_tuple.index(3) = {index_3}\n")

print("【 len(): 튜플의 길이 】")
length = len(numbers_tuple)
print(f"튜플의 길이: len(numbers_tuple) = {length}\n")

print("【 in: 요소가 있는지 확인 】")
is_in = 2 in numbers_tuple
print(f"2가 있나? 2 in numbers_tuple = {is_in}")

# ============================================================================
# 파트 5: 튜플의 응용
# ============================================================================

print("\n" + "-" * 80)
print("파트 5: 튜플의 실제 응용")
print("-" * 80)

print("\n응용 1: 함수에서 여러 값 반환\n")

def get_person_info():
    name = "Bob"
    age = 30
    email = "bob@example.com"
    return (name, age, email)  # 튜플로 반환

result = get_person_info()
print(f"반환값: {result}")

name, age, email = result
print(f"이름: {name}, 나이: {age}, 이메일: {email}\n")

print("응용 2: 불변 기록 저장\n")

transaction = ("2026-02-24", 10000, "구매", "완료")
print(f"거래 기록: {transaction}")
print("→ 거래 기록은 절대 바뀔 수 없습니다!\n")

print("응용 3: 딕셔너리의 키로 사용\n")

locations = {
    (37.7749, -122.4194): "샌프란시스코",
    (34.0522, -118.2437): "로스앤젤레스",
    (40.7128, -74.0060): "뉴욕"
}

print(f"locations = {locations}")
print(f"좌표 (40.7128, -74.0060)의 도시: {locations[(40.7128, -74.0060)]}")

# ============================================================================
# 파트 6: 집합의 필요성 - 중복 제거
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 6: 집합(Set) - 중복 없는 모음 】")
print("=" * 80)

print("\n상황: 학생들의 신청 과목을 관리하는데, 중복이 많아요!\n")

print("방법 1: 리스트 사용 (중복 있음!)")
courses_list = ["파이썬", "웹개발", "파이썬", "데이터베이스", "파이썬", "웹개발"]
print(f"courses_list = {courses_list}")
print(f"과목 개수: {len(courses_list)}개 (중복 포함!)")
print("→ 파이썬이 3번, 웹개발이 2번 중복되었어요! 😫\n")

print("방법 2: 집합 사용 (중복 자동 제제거!)")
courses_set = {"파이썬", "웹개발", "파이썬", "데이터베이스", "파이썬", "웹개발"}
print(f"courses_set = {courses_set}")
print(f"과목 개수: {len(courses_set)}개 (중복 제거됨!)")
print("→ 중복이 자동으로 제거되었어요! 🎉")

# ============================================================================
# 파트 7: 집합의 기본 구조
# ============================================================================

print("\n" + "-" * 80)
print("파트 7: 집합 만들고 사용하기")
print("-" * 80)

print("\n집합을 만드는 방법:\n")
print("set_name = {항목1, 항목2, 항목3}")
print("또는")
print("set_name = set([리스트])\n")

print("예시 1: 좋아하는 과일들\n")

fruits_set = {"사과", "바나나", "딸기", "포도"}
print(f"fruits_set = {fruits_set}")
print(f"과일 종류: {len(fruits_set)}개")

print("\n중복이 있으면 자동 제거됨:\n")

fruits_with_dup = {"사과", "바나나", "사과", "딸기", "바나나"}
print(f"입력: {fruits_with_dup}")
print("→ 중복이 제거되었어요!\n")

print("예시 2: 출석 학생 목록\n")

present_students = {"Alice", "Bob", "Charlie", "Diana"}
print(f"present_students = {present_students}")
print(f"출석 인원: {len(present_students)}명")

# ============================================================================
# 파트 8: 집합의 연산
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 8: 집합의 마법 — 합집합, 교집합, 차집합 】")
print("=" * 80)

print("\n수학 시간에 배운 집합 연산이 파이썬에서도 가능해요!\n")

class_a = {"Alice", "Bob", "Charlie"}
class_b = {"Bob", "Diana", "Eve"}

print(f"class_a = {class_a}")
print(f"class_b = {class_b}\n")

print("【 합집합(Union) - 모든 학생 】\n")

union = class_a | class_b
print(f"class_a | class_b = {union}")
print("→ 두 반의 모든 학생을 합쳤어요!\n")

print("【 교집합(Intersection) - 공통 학생 】\n")

intersection = class_a & class_b
print(f"class_a & class_b = {intersection}")
print("→ 두 반에 모두 있는 학생은 Bob뿐이에요!\n")

print("【 차집합(Difference) - A에만 있는 학생 】\n")

difference = class_a - class_b
print(f"class_a - class_b = {difference}")
print("→ class_a에만 있고 class_b에는 없는 학생들이에요!\n")

# ============================================================================
# 파트 9: 집합의 메서드
# ============================================================================

print("\n" + "-" * 80)
print("파트 9: 집합의 유용한 메서드")
print("-" * 80)

print("\n집합은 리스트/튜플과 달리 '추가/제거'가 가능해요!\n")

colors = {"빨강", "초록", "파랑"}
print(f"colors = {colors}\n")

print("【 add(): 요소 추가 】")
colors.add("노랑")
print(f'colors.add("노랑"): {colors}\n')

print("【 remove(): 요소 제거 】")
colors.remove("초록")
print(f'colors.remove("초록"): {colors}\n')

print("【 discard(): 안전하게 제거 】")
colors.discard("주황")  # 없어도 에러 없음
print(f'colors.discard("주황"): {colors}\n')

print("【 clear(): 모두 삭제 】")
test_set = {1, 2, 3}
test_set.clear()
print(f"clear() 후: {test_set}\n")

print("【 pop(): 임의로 하나 꺼내기 】")
numbers = {10, 20, 30, 40}
popped = numbers.pop()
print(f"pop() 결과: {popped}")
print(f"남은 집합: {numbers}")

# ============================================================================
# 파트 10: 세 가지 자료구조 비교
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 10: 리스트 vs 튜플 vs 집합 vs 딕셔너리 】")
print("=" * 80)

print("\n데이터 저장 방식을 선택하는 기준:\n")

print("【 리스트 [ ] 】")
print("  • 순서가 중요함")
print("  • 수정 가능")
print("  • 중복 허용")
print("  • 사용례: 시간 순서대로 저장한 데이터")
print("  예: [2026, 2, 24, 10, 30]\n")

print("【 튜플 ( ) 】")
print("  • 순서가 중요함")
print("  • 수정 불가능 (안전)")
print("  • 중복 허용")
print("  • 사용례: 날짜, 좌표, 불변 기록")
print("  예: (2026, 2, 24)\n")

print("【 집합 { } 】")
print("  • 순서 없음")
print("  • 수정 가능")
print("  • 중복 불허용 (자동 제거)")
print("  • 사용례: 유일한 항목들, 수학 연산")
print("  예: {'파이썬', '웹개발'}\n")

print("【 딕셔너리 { } 】")
print("  • 키-값 쌍")
print("  • 수정 가능")
print("  • 의미 있는 이름으로 접근")
print("  • 사용례: 학생 정보, 설정값")
print("  예: {'이름': 'Alice', '나이': 25}")

# ============================================================================
# 파트 11: 실제 응용
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 11: 실제 응용 — 중복 제거 및 데이터 분석 】")
print("=" * 80)

print("\n상황: 방문자의 IP 주소를 기록했는데, 중복이 많아요!\n")

ip_logs = [
    "192.168.1.1",
    "192.168.1.2",
    "192.168.1.1",
    "192.168.1.3",
    "192.168.1.2",
    "192.168.1.1"
]

print(f"전체 접속 기록: {len(ip_logs)}개")
print(f"기록: {ip_logs}\n")

unique_ips = set(ip_logs)
print(f"유일한 IP 주소: {len(unique_ips)}개")
print(f"IP 목록: {unique_ips}\n")

print("【 분석 】")
print(f"  • 방문자가 중복 제거 후 {len(unique_ips)}명")
print(f"  • 중복으로 인한 중복 방문: {len(ip_logs) - len(unique_ips)}회\n")

print("\n응용 2: 과목 선택 시스템\n")

student1_courses = {"파이썬", "웹개발", "데이터베이스"}
student2_courses = {"파이썬", "C++", "알고리즘"}
student3_courses = {"웹개발", "알고리즘", "보안"}

all_courses = student1_courses | student2_courses | student3_courses
common_courses = student1_courses & student2_courses

print(f"학생1 과목: {student1_courses}")
print(f"학생2 과목: {student2_courses}")
print(f"학생3 과목: {student3_courses}")
print(f"\n개설된 전체 과목: {all_courses}")
print(f"학생1, 2가 모두 듣는 과목: {common_courses}")

# ============================================================================
# 최종 정리
# ============================================================================

print("\n" + "=" * 80)
print("【 오늘의 학습 정리 】")
print("=" * 80)

print("\n튜플(Tuple):")
print("  • 생성: (항목1, 항목2)")
print("  • 특징: 불변(Immutable) - 수정/추가/삭제 불가")
print("  • 메서드: count(), index(), len(), in")
print("  • 용도: 불변 기록, 함수 반환값, 딕셔너리 키")

print("\n집합(Set):")
print("  • 생성: {항목1, 항목2} 또는 set(리스트)")
print("  • 특징: 중복 제거, 순서 없음")
print("  • 메서드: add(), remove(), pop(), clear()")
print("  • 연산: | (합집합), & (교집합), - (차집합)")
print("  • 용도: 중복 제거, 수학 연산")

print("\n네 가지 자료구조의 선택 기준:")
print("  ┌─────────────────────────────────────┐")
print("  │ 순서? │ 수정? │ 중복? │  ↓ 자료구조 │")
print("  ├─────────────────────────────────────┤")
print("  │  ⭕  │  ⭕  │  ⭕  │   리스트    │")
print("  │  ⭕  │  ❌  │  ⭕  │   튜플      │")
print("  │  ❌  │  ⭕  │  ❌  │   집합      │")
print("  │  이름 │  ⭕  │  ⭕  │  딕셔너리   │")
print("  └─────────────────────────────────────┘")

print("\n【 중학교 1학년까지의 데이터 구조 진화 】")
print("  v1.3: 리스트 [ ]      → 자유로운 순서")
print("  v1.7: 딕셔너리 { }    → 의미 있는 이름")
print("  v1.8: 튜플 ( )        → 변하지 않는 기록")
print("       집합 { }         → 중복 없는 모음")
print("  = 프로그래밍의 데이터 설계 능력 완성! 🎯")

# ============================================================================
# 마법의 말
# ============================================================================

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n💡 오늘의 깨달음:")
print("   '불변성'과 '유일성' - 프로그래밍의 핵심 개념들입니다!")
print("   세상의 모든 데이터가 바뀔 수 있는 것은 아니고,")
print("   모든 데이터가 중복될 필요는 없습니다.")
print("   올바른 자료구조를 선택하는 것이 좋은 코드의 시작입니다! 🏗️")

print("\n🎒 다음 시간에는:")
print("   [v1.9: 파일 입출력(File I/O) — 데이터의 영속성]")
print("   메모리에만 있던 데이터를 파일로 저장하고,")
print("   다시 불러오는 방법을 배워요!")

print("\n축하합니다! 👏")
print("이제 여러분은 상황에 맞는 최적의 자료구조를 선택할 수 있습니다!")
