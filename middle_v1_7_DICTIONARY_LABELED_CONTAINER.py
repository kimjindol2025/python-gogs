#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🎒 파이썬 중학교 1학년 - v1.7: 딕셔너리(Dictionary) —                      ║
║                    이름표로 데이터 묶기                                       ║
║  [Middle School Python: Dictionary - Labeled Data Container]                 ║
║                                                                               ║
║  초등학교에서는 리스트라는 '순서가 있는 바구니'를 배웠습니다.               ║
║  하지만 현실의 데이터는 항상 순서대로 정렬되어 있지 않습니다!              ║
║                                                                               ║
║  예를 들어:                                                                  ║
║  ["Alice", 28, "프로그래머"]라고 하면                                        ║
║  어느 것이 이름이고, 어느 것이 나이이고, 어느 것이 직업인지                ║
║  번호를 세어야만 알 수 있습니다!                                            ║
║                                                                               ║
║  하지만 {'이름': 'Alice', '나이': 28, '직업': '프로그래머'}라면             ║
║  한눈에 알 수 있죠?                                                          ║
║                                                                               ║
║  이것이 바로 딕셔너리(Dictionary)입니다!                                    ║
║  '키(Key)'라는 이름표를 붙여서 데이터를 저장하는 방식입니다.               ║
║                                                                               ║
║  리스트: 숫자로 찾는다 (list[0])                                            ║
║  딕셔너리: 이름으로 찾는다 (dict['name'])                                   ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🎒 파이썬 중학교 1학년 - v1.7: 딕셔너리(Dictionary) — 이름표로 데이터 묶기")
print("=" * 80)

# ============================================================================
# 파트 1: 리스트의 한계와 딕셔너리의 필요성
# ============================================================================

print("\n【 파트 1: 문제 상황 - 리스트만으로는 부족하다 】")
print("\n상황: 학생 정보를 저장하고 싶어요!\n")

print("방법 1: 리스트 사용 (번호로 찾기)")
print("---")
student_list = ["Alice", 28, "프로그래머", "서울"]
print(f"student_list = {student_list}")
print(f"이름: student_list[0] = {student_list[0]}")
print(f"나이: student_list[1] = {student_list[1]}")
print(f"직업: student_list[2] = {student_list[2]}")
print(f"도시: student_list[3] = {student_list[3]}")
print("---\n")

print("문제점:")
print("  ❌ 어느 것이 어느 정보인지 헷갈린다")
print("  ❌ 4번째 정보가 뭐였더라?")
print("  ❌ 인덱스를 계속 세어야 한다\n")

print("방법 2: 딕셔너리 사용 (이름으로 찾기)")
print("---")
student_dict = {
    "이름": "Alice",
    "나이": 28,
    "직업": "프로그래머",
    "도시": "서울"
}
print(f'student_dict = {student_dict}')
print(f'이름: student_dict["이름"] = {student_dict["이름"]}')
print(f'나이: student_dict["나이"] = {student_dict["나이"]}')
print(f'직업: student_dict["직업"] = {student_dict["직업"]}')
print(f'도시: student_dict["도시"] = {student_dict["도시"]}')
print("---\n")

print("장점:")
print("  ✅ 어느 것이 어느 정보인지 명확하다")
print("  ✅ 이름으로 바로 찾을 수 있다")
print("  ✅ 훨씬 읽기 쉽다! 🎉")

# ============================================================================
# 파트 2: 딕셔너리의 기본 구조
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 딕셔너리의 구조 】")
print("=" * 80)

print("\n딕셔너리를 만드는 방법:\n")
print("dict_name = {")
print("    '키1': 값1,")
print("    '키2': 값2,")
print("    '키3': 값3")
print("}")

print("\n예시: 책 정보를 딕셔너리로 저장\n")

book = {
    "제목": "파이썬의 정석",
    "저자": "클로드",
    "출판년도": 2026,
    "페이지": 500,
    "가격": 35000
}

print("코드:")
print('book = {')
print('    "제목": "파이썬의 정석",')
print('    "저자": "클로드",')
print('    "출판년도": 2026,')
print('    "페이지": 500,')
print('    "가격": 35000')
print('}')
print()

print("결과:")
print(f"book = {book}\n")

print("【 중요한 개념 】")
print("  • 키(Key): 데이터를 찾을 때 사용하는 이름표")
print("  • 값(Value): 실제 저장된 데이터")
print("  • 쌍(Pair): 키와 값이 함께 저장됨")
print("  • 콜론(:): 키와 값을 구분하는 기호")
print("  • 중괄호({}): 딕셔너리를 표현하는 기호 (리스트는 [])")

# ============================================================================
# 파트 3: 딕셔너리에서 값 꺼내기
# ============================================================================

print("\n" + "-" * 80)
print("파트 3: 딕셔너리에서 값 꺼내기 (접근)")
print("-" * 80)

print("\n방법 1: 키로 직접 접근\n")

print("코드:")
print('title = book["제목"]')
print('print(f"책 제목: {title}")\n')

print("실행 결과:")
title = book["제목"]
print(f"책 제목: {title}\n")

print("다른 예시들:\n")

author = book["저자"]
year = book["출판년도"]
price = book["가격"]

print(f"저자: {author}")
print(f"출판년도: {year}년")
print(f"가격: {price}원")

print("\n\n방법 2: get() 메서드 사용 (안전한 방법)\n")

print("코드:")
print('subtitle = book.get("부제목")')
print('print(subtitle)\n')

print("실행 결과:")
subtitle = book.get("부제목")
print(f"부제목: {subtitle}")

print("\n【 차이점 】")
print('  • book["부제목"] → 키가 없으면 에러!')
print('  • book.get("부제목") → 키가 없으면 None을 돌려줌')
print('  • book.get("부제목", "정보 없음") → 기본값 설정 가능')

subtitle_safe = book.get("부제목", "정보 없음")
print(f"\n안전한 방법: {subtitle_safe}")

# ============================================================================
# 파트 4: 딕셔너리에 데이터 추가/수정하기
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 4: 딕셔너리 수정하기 — 추가 및 변경 】")
print("=" * 80)

print("\n상황: 책 정보를 수정하고 새로운 정보를 추가하고 싶어요!\n")

print("원본:")
print(f"book = {book}\n")

print("작업 1: 기존 값 수정하기\n")

print("코드: book['가격'] = 40000")
book["가격"] = 40000
print(f"결과: {book['가격']}원으로 인상됨\n")

print("작업 2: 새로운 정보 추가하기\n")

print("코드: book['출판사'] = '클로드 출판'")
book["출판사"] = "클로드 출판"
print(f"결과: book = {book}\n")

print("작업 3: 평점 추가하기\n")

print("코드: book['평점'] = 4.8")
book["평점"] = 4.8
print(f"결과: {book}\n")

print("【 규칙 】")
print("  • 키가 없으면: 새로운 데이터가 추가된다")
print("  • 키가 있으면: 기존 데이터가 수정된다")

# ============================================================================
# 파트 5: 딕셔너리 삭제하기
# ============================================================================

print("\n" + "-" * 80)
print("파트 5: 딕셔너리에서 데이터 삭제하기")
print("-" * 80)

print("\n상황: 정보를 삭제하고 싶어요!\n")

print(f"현재 딕셔너리: {book}\n")

print("작업: 평점 정보 삭제\n")

print("코드: del book['평점']")
del book["평점"]
print(f"결과: {book}\n")

print("【 삭제 방법 】")
print("  • del dict['키']: 완전히 제거")
print("  • dict.pop('키'): 제거하면서 값을 받기")

price_removed = book.pop("가격")
print(f"\npop으로 제거: {price_removed}원을 제거했습니다")
print(f"이제 book = {book}")

# ============================================================================
# 파트 6: 딕셔너리의 키, 값, 쌍 보기
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 6: 딕셔너리의 모든 정보 살펴보기 】")
print("=" * 80)

print("\n새 학생 정보를 만들어봅시다:\n")

student = {
    "이름": "Bob",
    "나이": 25,
    "학년": 3,
    "성적": 4.5
}

print(f"student = {student}\n")

print("【 keys(): 모든 키 보기 】\n")

print("코드: student.keys()")
print("결과:")
keys = student.keys()
print(f"  {keys}\n")

print("【 values(): 모든 값 보기 】\n")

print("코드: student.values()")
print("결과:")
values = student.values()
print(f"  {values}\n")

print("【 items(): 모든 키-값 쌍 보기 】\n")

print("코드: student.items()")
print("결과:")
items = student.items()
print(f"  {items}\n")

# ============================================================================
# 파트 7: 딕셔너리와 반복문
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 7: 딕셔너리와 반복문 — 모든 데이터 순회하기 】")
print("=" * 80)

print("\n상황 1: 모든 키에 대해 반복\n")

print("코드:")
print("for key in student:")
print("    print(key)\n")

print("실행 결과:\n")

for key in student:
    print(f"  {key}")

print("\n\n상황 2: 모든 값에 대해 반복\n")

print("코드:")
print("for value in student.values():")
print("    print(value)\n")

print("실행 결과:\n")

for value in student.values():
    print(f"  {value}")

print("\n\n상황 3: 모든 키-값 쌍에 대해 반복 (가장 유용!)\n")

print("코드:")
print("for key, value in student.items():")
print("    print(f'{key}: {value}')\n")

print("실행 결과:\n")

for key, value in student.items():
    print(f"  {key}: {value}")

# ============================================================================
# 파트 8: 딕셔너리와 조건문
# ============================================================================

print("\n" + "-" * 80)
print("파트 8: 딕셔너리와 조건문 — 키 확인하기")
print("-" * 80)

print("\n상황: 특정 정보가 있는지 확인하고 싶어요!\n")

print("코드:")
print('if "성적" in student:')
print('    print("성적 정보가 있습니다!")')
print('else:')
print('    print("성적 정보가 없습니다!")\n')

print("실행 결과:\n")

if "성적" in student:
    print("  성적 정보가 있습니다!")
else:
    print("  성적 정보가 없습니다!")

print("\n다른 예시:\n")

if "주소" in student:
    print("  주소 정보가 있습니다!")
else:
    print("  주소 정보가 없습니다!")

# ============================================================================
# 파트 9: 실제 응용 — 학생 정보 관리 시스템
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 9: 실제 응용 — 학생 정보 관리 】")
print("=" * 80)

print("\n상황: 여러 학생의 정보를 딕셔너리로 관리합니다!\n")

students = {
    "Alice": {"나이": 28, "학년": 3, "성적": 4.8},
    "Bob": {"나이": 25, "학년": 2, "성적": 4.2},
    "Charlie": {"나이": 26, "학년": 3, "성적": 4.5},
    "Diana": {"나이": 24, "학년": 1, "성적": 4.9}
}

print("코드 구조:")
print("students = {")
print("    '학생이름': {'정보키': 값, ...},")
print("    ...}")
print()

print("작업 1: Alice의 학년 확인\n")

alice_grade = students["Alice"]["학년"]
print(f"Alice의 학년: {alice_grade}학년\n")

print("작업 2: 모든 학생의 이름과 성적 보기\n")

for name, info in students.items():
    grade = info["성적"]
    print(f"  {name}: {grade}점")

print("\n작업 3: 성적이 4.5 이상인 학생만 출력\n")

for name, info in students.items():
    if info["성적"] >= 4.5:
        print(f"  ⭐ {name}: {info['성적']}점")

print("\n작업 4: 새로운 학생 추가\n")

students["Eve"] = {"나이": 27, "학년": 2, "성적": 4.3}
print(f"Eve 추가 완료!")
print(f"현재 학생 수: {len(students)}명")

# ============================================================================
# 파트 10: 딕셔너리의 유용한 메서드
# ============================================================================

print("\n" + "-" * 80)
print("파트 10: 유용한 딕셔너리 메서드들")
print("-" * 80)

print("\n테스트용 딕셔너리:\n")

person = {"이름": "파이썬", "나이": 10, "도시": "서울"}
print(f"person = {person}\n")

print("【 len(): 데이터 개수 】")
print(f"len(person) = {len(person)} (3개의 키-값 쌍)")

print("\n【 clear(): 모두 삭제 】")
test_dict = {"a": 1, "b": 2, "c": 3}
print(f"삭제 전: {test_dict}")
test_dict.clear()
print(f"삭제 후: {test_dict}")

print("\n【 update(): 여러 데이터 한 번에 추가 】")
skills = {"파이썬": 90, "자바": 75}
new_skills = {"C++": 80, "JavaScript": 85}
print(f"원본: {skills}")
skills.update(new_skills)
print(f"update 후: {skills}")

print("\n【 copy(): 딕셔너리 복사 】")
original = {"x": 10, "y": 20}
copied = original.copy()
copied["x"] = 100
print(f"원본: {original}")
print(f"복사본 (수정됨): {copied}")
print("→ 복사본을 수정해도 원본은 변하지 않음!")

# ============================================================================
# 파트 11: 리스트와 딕셔너리 비교
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 11: 리스트 vs 딕셔너리 】")
print("=" * 80)

print("\n정보를 저장하는 두 가지 방법:\n")

print("【 리스트: 순서가 중요할 때 】")
test_scores = [95, 87, 92, 78]
print(f"test_scores = {test_scores}")
print(f"첫 번째 점수: test_scores[0] = {test_scores[0]}")
print("→ 순서대로 데이터를 저장합니다")

print("\n【 딕셔너리: 의미가 중요할 때 】")
scores_dict = {
    "국어": 95,
    "영어": 87,
    "수학": 92,
    "과학": 78
}
print(f"scores_dict = {scores_dict}")
print(f"수학 점수: scores_dict['수학'] = {scores_dict['수학']}")
print("→ 각 데이터의 의미를 명확하게 표현합니다")

print("\n【 선택 기준 】")
print("  리스트 사용: 순서가 있는 자료 (성적 추이, 시간 순서 등)")
print("  딕셔너리 사용: 관계있는 정보의 묶음 (학생 정보, 책 정보 등)")

# ============================================================================
# 최종 정리
# ============================================================================

print("\n" + "=" * 80)
print("【 오늘의 학습 정리 】")
print("=" * 80)

print("\n딕셔너리(Dictionary)의 기본 구조:")
print('  dict_name = {"키1": 값1, "키2": 값2, ...}')

print("\n딕셔너리의 주요 기능:")
print('  • 생성: {"key": value}')
print('  • 접근: dict["key"]')
print('  • 추가/수정: dict["new_key"] = value')
print('  • 삭제: del dict["key"]')
print('  • 키 확인: "key" in dict')

print("\n딕셔너리의 유용한 메서드:")
print('  • keys(): 모든 키 보기')
print('  • values(): 모든 값 보기')
print('  • items(): 모든 키-값 쌍 보기')
print('  • get(): 안전하게 값 가져오기')
print('  • pop(): 값을 가져오면서 삭제')
print('  • update(): 여러 데이터 추가')
print('  • clear(): 모든 데이터 삭제')

print("\n【 초등학교 vs 중학교 】")
print("  초등학교 리스트(v1.3): [데이터1, 데이터2, ...]")
print("  → 번호로 찾는다: list[0]")
print()
print("  중학교 딕셔너리(v1.7): {'이름': 데이터, ...}")
print("  → 이름으로 찾는다: dict['이름']")
print()
print("  시간이 지남에 따라 데이터 구조는 더 정교해진다! 📈")

# ============================================================================
# 마법의 말
# ============================================================================

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n💡 오늘의 깨달음:")
print("   딕셔너리는 '의미 있는 데이터 저장'의 시작입니다!")
print("   번호로 찾는 리스트에서 벗어나,")
print("   이름으로 찾는 딕셔너리의 세계로 진입했습니다.")
print("   이것이 '실제 세계의 데이터'에 더 가까운 표현입니다! 🎯")

print("\n🎒 다음 시간에는:")
print("   [v1.8: 튜플(Tuple) — 변경할 수 없는 리스트]")
print("   불변(Immutable) 데이터의 개념을 배우고,")
print("   딕셔너리와 함께 더 강력한 데이터 구조를 만들어봅니다!")

print("\n축하합니다! 👏")
print("이제 여러분은 '의미 있는 데이터 저장소'를 만들 수 있습니다!")
