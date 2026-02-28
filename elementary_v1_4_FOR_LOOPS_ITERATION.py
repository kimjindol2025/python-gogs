#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🎒 파이썬 초등학교 1학년 - v1.4: 반복문(for) — 바구니 안의 데이터           ║
║                                        모두 살펴보기                          ║
║  [Elementary Python: For Loops - Iteration]                                  ║
║                                                                               ║
║  v1.3에서는 리스트의 데이터를 하나씩 번호표로 꺼냈습니다.                   ║
║  하지만 데이터가 1000개라면? 10000개라면?                                   ║
║  하나씩 타이핑할 수는 없겠죠?                                                ║
║                                                                               ║
║  그래서 파이썬은 '반복문(for)'이라는 마법의 주문을 제공합니다!              ║
║  이것이 프로그래밍에서 가장 중요한 개념 중 하나입니다.                       ║
║                                                                               ║
║  for 반복문은 바구니 안의 모든 데이터를 자동으로 살펴봅니다.                ║
║  마치 "각 과일마다 하나씩 골라서 확인하기"처럼요!                           ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🎒 파이썬 초등학교 1학년 - v1.4: 반복문(for) — 바구니 안의 데이터 모두 살펴보기")
print("=" * 80)

# ============================================================================
# 파트 1: 반복문 없이 데이터 처리하기 (문제점)
# ============================================================================

print("\n【 파트 1: 문제 상황 - 반복문 없이는? 】")
print("\n상황: 과일 바구니에서 모든 과일을 하나씩 꺼내서 보고 싶어요!\n")

fruits = ["사과", "바나나", "포도", "딸기", "수박"]

print(f"fruits = {fruits}")
print("\n현재까지 배운 방법 (번호표로 하나씩):")
print(f"  fruits[0] = {fruits[0]}")
print(f"  fruits[1] = {fruits[1]}")
print(f"  fruits[2] = {fruits[2]}")
print(f"  fruits[3] = {fruits[3]}")
print(f"  fruits[4] = {fruits[4]}")

print("\n만약 과일이 100개라면? 1000개라면?")
print("이렇게 일일이 타이핑할 수는 없어요! 😫")
print("\n이때 우리가 필요한 것이 바로 '반복문(for)'입니다!")

# ============================================================================
# 파트 2: 반복문의 기본 (첫 번째 마법)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 마법의 주문 — for 반복문 】")
print("=" * 80)

print("\n가장 기본적인 for 반복문의 모양:")
print("\nfor fruit in fruits:")
print("    print(fruit)")

print("\n의미:")
print("  1. fruits라는 바구니에서")
print("  2. 하나씩 데이터를 꺼내서")
print("  3. fruit이라는 임시 상자에 담고")
print("  4. 아래의 들여쓴 코드를 반복 실행")

print("\n실제로 실행해봅시다:\n")

for fruit in fruits:
    print(f"  {fruit}")

print("\n신기하죠? 모든 과일이 자동으로 출력되었어요! ✨")

# ============================================================================
# 파트 3: 반복문 안의 들여쓰기 (중요한 규칙)
# ============================================================================

print("\n" + "-" * 80)
print("파트 3: 반복문의 가장 중요한 규칙 — 들여쓰기(Indentation)")
print("-" * 80)

print("\n【 들여쓰기가 중요한 이유 】\n")

print("✓ 들여쓴 부분 (반복될 부분):")
print("  for fruit in fruits:")
print("      print(fruit)        # ← 이 부분이 반복됩니다")
print("      print('---')         # ← 이것도 반복됩니다")

print("\n✗ 들여쓰지 않은 부분 (반복이 끝난 후):")
print("  for fruit in fruits:")
print("      print(fruit)")
print("  print('끝!')             # ← 이것은 한 번만 실행됩니다")

print("\n예시를 봅시다:\n")

for fruit in fruits:
    print(f"확인 중: {fruit}")
    print("-" * 20)

print("✓ 반복이 완료되었습니다!")

# ============================================================================
# 파트 4: 반복문 안에서 작업하기
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 4: 반복문 안에서 계산하기 】")
print("=" * 80)

print("\n반복문은 단순히 출력만 하는 게 아니에요.")
print("반복문 안에서 계산도 할 수 있습니다!\n")

numbers = [1, 2, 3, 4, 5]

print("문제: 각 숫자의 2배를 출력하고 싶어요!\n")
print(f"numbers = {numbers}\n")

print("해결책:\n")
print("for num in numbers:")
print("    doubled = num * 2")
print("    print(f'{num}의 2배 = {doubled}')\n")

print("실행 결과:\n")

for num in numbers:
    doubled = num * 2
    print(f"  {num}의 2배 = {doubled}")

# ============================================================================
# 파트 5: 반복문의 반복 변수 이해하기
# ============================================================================

print("\n" + "-" * 80)
print("파트 5: 반복 변수(Loop Variable) — fruit, num은 뭐예요?")
print("-" * 80)

print("\n반복할 때마다 fruit과 num은 계속 바뀝니다!\n")

students = ["Alice", "Bob", "Charlie"]

print(f"students = {students}\n")
print("for student in students:")
print("    print(f'반복 변수 값: {student}')\n")
print("실행:\n")

for student in students:
    print(f"  현재 student 값: '{student}'")

print("\n각 반복마다 student이 새로운 값으로 업데이트되는 거랍니다!")
print("  1번째: student = 'Alice'")
print("  2번째: student = 'Bob'")
print("  3번째: student = 'Charlie'")
print("  → 반복 끝!")

# ============================================================================
# 파트 6: 숫자 범위로 반복하기 (range 함수)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 6: 숫자로 반복하기 — range() 함수 】")
print("=" * 80)

print("\n때로는 리스트 없이 단순히 숫자를 반복하고 싶을 수도 있어요.")
print("예: 1번부터 5번까지 반복하기\n")

print("방법 1: 직접 숫자를 세어서 range() 사용\n")

print("코드: for i in range(5):")
print("          print(i)\n")

print("결과:\n")

for i in range(5):
    print(f"  {i}")

print("\n[ 중요한 규칙 ]")
print("  range(5) = [0, 1, 2, 3, 4]")
print("  → 0부터 4까지 (5는 포함 안 됨!)")
print("  → 이것도 0부터 시작합니다!")

print("\n\n다른 range 예시:\n")

print("range(3, 8):  (3부터 7까지)")
for i in range(3, 8):
    print(f"  {i}", end="  ")
print()

print("\nrange(1, 11, 2):  (1부터 10까지, 2칸씩 건너뛰기)")
for i in range(1, 11, 2):
    print(f"  {i}", end="  ")
print()

# ============================================================================
# 파트 7: 리스트와 range를 함께 사용하기
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 7: 번호표로도 반복하기 — range와 len 조합 】")
print("=" * 80)

print("\n때로는 '몇 번째인지'도 알고 싶을 수 있어요.\n")

colors = ["빨강", "초록", "파랑"]

print(f"colors = {colors}\n")

print("방법 1: range와 len을 조합하기\n")
print("코드: for i in range(len(colors)):")
print("          print(f'{i}번째: {colors[i]}')\n")

print("실행 결과:\n")

for i in range(len(colors)):
    print(f"  {i}번째: {colors[i]}")

print("\n설명:")
print(f"  • len(colors) = {len(colors)}")
print("  • range(3) = [0, 1, 2]")
print("  • i가 0, 1, 2 순서대로 반복됨")

# ============================================================================
# 파트 8: 실제 응용 — 학생 성적 처리
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 8: 실제 응용 — 학생 성적 처리 】")
print("=" * 80)

print("\n상황: 학생들의 성적이 리스트에 저장되어 있어요.")
print("모든 학생의 성적을 확인하고 평가해봅시다!\n")

scores = [85, 92, 78, 95, 88]

print(f"scores = {scores}\n")

print("【 작업 1: 모든 성적 출력 】\n")

for score in scores:
    print(f"  점수: {score}점")

print("\n【 작업 2: 성적 평가 】\n")

for score in scores:
    if score >= 90:
        grade = "A 등급 (우수!)"
    elif score >= 80:
        grade = "B 등급 (좋음)"
    else:
        grade = "C 등급 (노력 중)"
    print(f"  {score}점 → {grade}")

print("\n【 작업 3: 성적 통계 】\n")

total = 0
for score in scores:
    total = total + score

average = total / len(scores)

print(f"  총합: {total}점")
print(f"  개수: {len(scores)}명")
print(f"  평균: {average}점")

# ============================================================================
# 파트 9: 중첩된 반복문 (반복 안의 반복)
# ============================================================================

print("\n" + "-" * 80)
print("파트 9: 반복 안의 반복 — 중첩 반복문")
print("-" * 80)

print("\n반복문 안에 또 다른 반복문을 넣을 수 있어요!\n")

print("예: 구구단 2단 출력\n")

print("코드:")
print("for i in range(1, 10):")
print("    print(f'2 × {i} = {2 * i}')\n")

print("실행:\n")

for i in range(1, 10):
    print(f"  2 × {i} = {2 * i}")

print("\n\n더 재미있는 예: 표 만들기\n")

print("코드:")
print("for i in range(3):")
print("    for j in range(3):")
print("        print('★', end=' ')")
print("    print()  # 줄바꿈\n")

print("실행:\n")

for i in range(3):
    for j in range(3):
        print("  ★", end=" ")
    print()

print("\n이렇게 반복 안에 반복을 넣으면 복잡한 패턴도 만들 수 있어요!")

# ============================================================================
# 파트 10: 반복문 제어하기 (break, continue)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 10: 반복문 제어하기 — break와 continue 】")
print("=" * 80)

print("\n때로는 반복을 도중에 멈추거나 건너뛰고 싶을 수 있어요.\n")

print("【 break: 반복 즉시 중단 】\n")

print("상황: 숫자 1부터 10까지 세는데, 5를 만나면 멈추기\n")

print("for num in range(1, 11):")
print("    if num == 5:")
print("        break  # 반복 즉시 중단")
print("    print(num)\n")

print("실행:\n")

for num in range(1, 11):
    if num == 5:
        break
    print(f"  {num}")

print("→ 5가 되면 반복이 멈았어요!\n")

print("\n【 continue: 현재 반복 건너뛰기 】\n")

print("상황: 1부터 10까지 세는데, 짝수는 건너뛰기\n")

print("for num in range(1, 11):")
print("    if num % 2 == 0:")
print("        continue  # 이번 반복만 건너뛰기")
print("    print(num)\n")

print("실행:\n")

for num in range(1, 11):
    if num % 2 == 0:
        continue
    print(f"  {num}")

print("→ 짝수(2, 4, 6, 8, 10)는 출력되지 않았어요!")

# ============================================================================
# 파트 11: enumerate — 번호와 데이터 함께 얻기
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 11: enumerate() — 번호표와 데이터 함께 얻기 】")
print("=" * 80)

print("\n v1.7에서 배울 더 편한 방법 미리보기!\n")

fruits_list = ["사과", "바나나", "포도"]

print(f"fruits_list = {fruits_list}\n")

print("range(len())을 사용한 방법:")
for i in range(len(fruits_list)):
    print(f"  {i}번째: {fruits_list[i]}")

print("\nenumerate()를 사용한 더 편한 방법:\n")

for index, fruit in enumerate(fruits_list):
    print(f"  {index}번째: {fruit}")

print("\n 같은 결과지만 더 읽기 쉽지 않나요? ✨")
print("(이건 v1.7에서 자세히 배워요!)")

# ============================================================================
# 최종 정리
# ============================================================================

print("\n" + "=" * 80)
print("【 오늘의 학습 정리 】")
print("=" * 80)

print("\n반복문(for)의 기본 구조:")
print("  for 변수 in 리스트:")
print("      반복될 코드")

print("\n반복문의 핵심:")
print("  ✓ 리스트의 모든 데이터를 자동으로 처리")
print("  ✓ 반복 변수는 매번 새로운 값으로 업데이트")
print("  ✓ 들여쓰기가 중요함 (들여쓴 부분만 반복)")
print("  ✓ range()로 숫자 범위도 반복 가능")
print("  ✓ break로 중단, continue로 건너뛰기 가능")

print("\n반복문의 활용:")
print("  • 리스트의 모든 요소 처리")
print("  • 반복 계산 (합계, 평균, 최댓값 등)")
print("  • 조건에 따른 필터링")
print("  • 테이블/패턴 생성")
print("  • 특정 조건까지 실행")

print("\n【 0부터 시작과 반복문의 관계 】")
print("  반복문이 0부터 시작하는 이유도 같습니다.")
print("  컴퓨터는 메모리에서 '기준점으로부터")
print("  몇 칸 떨어져 있는가'로 위치를 찾기 때문입니다.")
print("  v1.3의 리스트 인덱싱과 v1.4의 반복문이")
print("  같은 원리를 공유하고 있습니다!")

# ============================================================================
# 마법의 말
# ============================================================================

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n💡 오늘의 깨달음:")
print("   for 반복문은 파이썬에서 가장 강력한 도구입니다!")
print("   수백 개, 수천 개의 데이터도")
print("   단 3줄의 코드로 처리할 수 있어요.")
print("   이것이 프로그래밍의 '자동화'입니다. ⚡")

print("\n🎒 다음 시간에는:")
print("   [v1.5: 조건문(if-else) — 분기점에서 선택하기]")
print("   반복문과 조건문을 함께 사용하면")
print("   훨씬 더 똑똑한 프로그램을 만들 수 있어요!")

print("\n잘했어요! 👏")
print("이제 여러분은 반복을 자동화할 수 있습니다!")
