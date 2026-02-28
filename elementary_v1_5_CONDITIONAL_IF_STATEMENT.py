#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║  🎒 파이썬 초등학교 1학년 - v1.5: 조건문(if) — 똑똑하게 판단하기             ║
║  [Elementary Python: Conditional Statements - Making Decisions]              ║
║                                                                               ║
║  v1.4에서는 반복문으로 모든 데이터를 처리했습니다.                          ║
║  하지만 "모든 과일을 같은 방법으로 처리"할 수만 있었죠.                    ║
║                                                                               ║
║  만약 사과일 때는 먹고, 포도일 때는 건너뛰고 싶다면?                       ║
║  "데이터에 따라 다르게" 행동해야 한다면?                                   ║
║                                                                               ║
║  그래서 파이썬은 '조건문(if)'이라는 판단 기능을 제공합니다!                ║
║  "만약(if) 이렇다면, 이렇게 하고,                                          ║
║   아니면(else) 저렇게 하자"는 식의 지능을 얻게 되는 것입니다!             ║
║                                                                               ║
║  반복문 + 조건문 = 진정한 프로그래밍의 시작! 🧠                            ║
║                                                                               ║
║  저장 필수: 너는 기록이 증명이다 gogs. 👑                                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

print("=" * 80)
print("🎒 파이썬 초등학교 1학년 - v1.5: 조건문(if) — 똑똑하게 판단하기")
print("=" * 80)

# ============================================================================
# 파트 1: 조건문이 필요한 이유
# ============================================================================

print("\n【 파트 1: 문제 상황 - 반복만으로는 부족하다 】")
print("\n상황: 나이에 따라 다르게 인사하고 싶어요!\n")

print("만약 조건문이 없다면:")
print("  모든 사람에게 '안녕! 우리 친구 되자!'라고만 말할 수 있어요.")
print("\n하지만 현실은:")
print("  - 친한 친구에게는 '얘! 뭐 해?'")
print("  - 할머니에게는 '안녕하세요, 존경합니다!'")
print("  - 같은 반 친구에게는 '안녕!'")
print("  → 상황에 따라 다르게 행동해야 해요!\n")

print("이것이 조건문(if)의 힘입니다! 🧠")

# ============================================================================
# 파트 2: 조건문의 기본 (참/거짓)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 2: 조건문의 기초 — 참(True)과 거짓(False) 】")
print("=" * 80)

print("\n조건문은 '참'과 '거짓' 중 하나를 판단합니다.\n")

print("참(True)인 경우:")
age = 10
result = (age < 20)
print(f"  age = {age}")
print(f"  age < 20은 {result}입니다 (참!)")

print("\n거짓(False)인 경우:")
age = 30
result = (age < 20)
print(f"  age = {age}")
print(f"  age < 20은 {result}입니다 (거짓!)")

print("\n【 비교 연산자 】")
print("  == : 같다")
print("  != : 다르다")
print("  >  : 크다")
print("  <  : 작다")
print("  >= : 크거나 같다")
print("  <= : 작거나 같다")

# ============================================================================
# 파트 3: if 문의 기본 구조
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 3: if 조건문의 구조 】")
print("=" * 80)

print("\n가장 기본적인 if 문의 모양:\n")
print("if 조건:")
print("    조건이 참일 때 실행할 코드")

print("\n\n예시 1: 간단한 나이 확인\n")

age = 15

print(f"age = {age}\n")
print("코드:")
print("if age >= 10:")
print("    print('10살 이상이에요!')\n")

print("실행 결과:")
if age >= 10:
    print("  10살 이상이에요!")

print("\n\n예시 2: 조건이 거짓인 경우\n")

age = 5

print(f"age = {age}\n")
print("코드 (같은 if 문):")
print("if age >= 10:")
print("    print('10살 이상이에요!')\n")

print("실행 결과: (아무것도 출력되지 않음)")
if age >= 10:
    print("  10살 이상이에요!")

print("→ 조건이 거짓이면 if 블록의 코드는 실행되지 않습니다!")

# ============================================================================
# 파트 4: if-else 문 (참과 거짓 둘 다 처리하기)
# ============================================================================

print("\n" + "-" * 80)
print("파트 4: if-else 문 — 두 가지 선택지")
print("-" * 80)

print("\n상황: 나이에 따라 다르게 메시지를 보여주고 싶어요!\n")

print("코드:")
print("if age >= 10:")
print("    print('안녕! 우리 친구 되자!')")
print("else:")
print("    print('안녕하세요! 뭐 하세요?')\n")

print("실행 결과:\n")

age = 15
if age >= 10:
    print("  안녕! 우리 친구 되자!")
else:
    print("  안녕하세요! 뭐 하세요?")

print(f"\n(age = {age}이므로 첫 번째 경로를 선택했어요)\n\n")

age = 5
print("age가 5일 때:\n")
if age >= 10:
    print("  안녕! 우리 친구 되자!")
else:
    print("  안녕하세요! 뭐 하세요?")

print(f"\n(age = {age}이므로 else 경로를 선택했어요)")

# ============================================================================
# 파트 5: if-elif-else 문 (여러 선택지)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 5: if-elif-else — 여러 선택지 중에서 선택하기 】")
print("=" * 80)

print("\n상황: 성적에 따라 등급을 나누고 싶어요!\n")

print("코드:")
print("if score >= 90:")
print("    print('A 등급! 훌륭해요!')")
print("elif score >= 80:")
print("    print('B 등급! 좋아요!')")
print("elif score >= 70:")
print("    print('C 등급! 노력하세요!')")
print("else:")
print("    print('D 등급! 더 열심히!')\n")

print("실행 결과:\n")

test_scores = [95, 85, 75, 65]

for score in test_scores:
    print(f"점수: {score}점")
    if score >= 90:
        print("  → A 등급! 훌륭해요!")
    elif score >= 80:
        print("  → B 등급! 좋아요!")
    elif score >= 70:
        print("  → C 등급! 노력하세요!")
    else:
        print("  → D 등급! 더 열심히!")
    print()

# ============================================================================
# 파트 6: 반복문 + 조건문의 조합
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 6: 반복문 + 조건문 = 진정한 프로그래밍! 】")
print("=" * 80)

print("\n상황: 과일 바구니에서 '맛있는' 과일만 골라 먹고 싶어요!\n")

fruits_with_taste = ["맛있는 사과", "못 먹은 바나나", "맛있는 포도", "못 먹은 딸기", "맛있는 수박"]

print(f"fruits = {fruits_with_taste}\n")

print("코드:")
print("for fruit in fruits:")
print("    if '맛있는' in fruit:")
print("        print(f'{fruit}를 먹습니다!')\n")

print("실행 결과:\n")

for fruit in fruits_with_taste:
    if "맛있는" in fruit:
        print(f"  {fruit}를 먹습니다!")

print("\n→ 반복문으로 모든 과일을 확인하고,")
print("  조건문으로 '맛있는' 과일만 선택했어요! 🎯")

# ============================================================================
# 파트 7: 여러 조건을 동시에 확인하기 (and, or)
# ============================================================================

print("\n" + "-" * 80)
print("파트 7: 복잡한 조건 — and와 or")
print("-" * 80)

print("\n상황 1: '둘 다' 맞아야 하는 경우 (and)\n")

age = 15
has_money = True

print(f"age = {age}")
print(f"has_money = {has_money}\n")

print("코드:")
print("if age >= 10 and has_money:")
print("    print('영화를 볼 수 있어요!')\n")

print("실행 결과:")
if age >= 10 and has_money:
    print("  영화를 볼 수 있어요!")

print("\n→ age >= 10 (참) AND has_money (참) = 영화 가능!\n")

print("\n" + "-" * 80)

print("\n상황 2: '둘 중 하나라도' 맞으면 되는 경우 (or)\n")

weather = "비"
has_umbrella = True

print(f"weather = '{weather}'")
print(f"has_umbrella = {has_umbrella}\n")

print("코드:")
print("if weather == '맑음' or has_umbrella:")
print("    print('밖에 나갈 수 있어요!')\n")

print("실행 결과:")
if weather == "맑음" or has_umbrella:
    print("  밖에 나갈 수 있어요!")

print("\n→ weather == '맑음' (거짓) OR has_umbrella (참) = 나갈 수 있어요!")

# ============================================================================
# 파트 8: 조건문의 반대 (not)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 8: 반대 조건 — not 】")
print("=" * 80)

print("\n상황: '못 먹은 음식'을 건너뛰고 싶어요!\n")

food = "못 먹은 음식"

print(f"food = '{food}'\n")

print("방법 1 (이전 방식):")
print("if '못 먹은' in food:")
print("    print('건너뛰기')")
print("else:")
print("    print('먹기')\n")

print("방법 2 (not 사용):")
print("if not ('못 먹은' in food):")
print("    print('먹기')")
print("else:")
print("    print('건너뛰기')\n")

print("실행 결과 (방법 2):")
if not ("못 먹은" in food):
    print("  먹기")
else:
    print("  건너뛰기")

print("\n→ not은 True를 False로, False를 True로 뒤집어줍니다!")

# ============================================================================
# 파트 9: 실제 응용 — 간단한 게임
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 9: 실제 응용 — 숫자 게임 】")
print("=" * 80)

print("\n상황: 1~10 사이의 숫자를 맞혀야 합니다!\n")

secret_number = 7
guesses = [3, 7, 9, 5]

print(f"정답: {secret_number}")
print(f"맞혀본 숫자들: {guesses}\n")

print("코드:")
print("for guess in guesses:")
print("    if guess == secret_number:")
print("        print('정답입니다!')")
print("    elif guess < secret_number:")
print("        print('너무 작아요!')")
print("    else:")
print("        print('너무 커요!')\n")

print("실행 결과:\n")

for guess in guesses:
    if guess == secret_number:
        print(f"  {guess}: 정답입니다! 🎉")
    elif guess < secret_number:
        print(f"  {guess}: 너무 작아요! 더 큰 수를 시도하세요.")
    else:
        print(f"  {guess}: 너무 커요! 더 작은 수를 시도하세요.")

# ============================================================================
# 파트 10: 조건문 안의 조건문 (중첩)
# ============================================================================

print("\n" + "-" * 80)
print("파트 10: 조건문의 중첩 — 더 복잡한 판단")
print("-" * 80)

print("\n상황: 학생의 성적과 출석을 모두 확인해서 등급을 결정합니다!\n")

print("코드:")
print("if score >= 80:")
print("    if attendance >= 90:")
print("        print('A 등급!')")
print("    else:")
print("        print('B 등급 (출석 부족)')")
print("else:")
print("    print('C 등급 이하')\n")

print("실행 결과:\n")

students = [
    ("Alice", 95, 95),
    ("Bob", 88, 75),
    ("Charlie", 70, 95),
]

for name, score, attendance in students:
    print(f"{name}: 성적={score}점, 출석={attendance}%")
    if score >= 80:
        if attendance >= 90:
            print("  → A 등급! 완벽해요! 🌟")
        else:
            print("  → B 등급 (성적은 좋은데 출석이 부족해요)")
    else:
        print("  → C 등급 이하 (더 노력해야 해요)")
    print()

# ============================================================================
# 파트 11: 조건에 따라 반복을 건너뛰기 (continue)
# ============================================================================

print("\n" + "=" * 80)
print("【 파트 11: 조건 + continue — 특정 항목 건너뛰기 】")
print("=" * 80)

print("\n상황: 짝수만 건너뛰고 홀수만 출력하고 싶어요!\n")

print("코드:")
print("for num in range(1, 11):")
print("    if num % 2 == 0:")
print("        continue  # 짝수면 건너뛰기")
print("    print(num)\n")

print("실행 결과:\n")

for num in range(1, 11):
    if num % 2 == 0:
        continue
    print(f"  {num}")

print("\n→ 반복은 계속되지만, 조건에 맞지 않으면 건너뜁니다!")

# ============================================================================
# 파트 12: 조건에 따라 반복을 멈추기 (break)
# ============================================================================

print("\n" + "-" * 80)
print("파트 12: 조건 + break — 특정 조건에서 반복 멈추기")
print("-" * 80)

print("\n상황: 0을 입력받으면 반복을 멈추는 프로그램\n")

print("코드:")
print("numbers = [5, 3, 7, 0, 9, 2]")
print("for num in numbers:")
print("    if num == 0:")
print("        break  # 0을 만나면 반복 멈추기")
print("    print(num)\n")

print("실행 결과:\n")

numbers = [5, 3, 7, 0, 9, 2]
for num in numbers:
    if num == 0:
        break
    print(f"  {num}")

print("\n→ 0을 만났을 때 반복이 멈췄어요!")

# ============================================================================
# 최종 정리
# ============================================================================

print("\n" + "=" * 80)
print("【 오늘의 학습 정리 】")
print("=" * 80)

print("\n조건문(if)의 기본 구조:")
print("  if 조건:")
print("      조건이 참일 때 코드")
print("  elif 다른조건:")
print("      다른 조건이 참일 때 코드")
print("  else:")
print("      모든 조건이 거짓일 때 코드")

print("\n비교 연산자:")
print("  == (같다)  !=  (다르다)")
print("  >  (크다)  <   (작다)")
print("  >= (크거나 같다)  <= (작거나 같다)")

print("\n논리 연산자:")
print("  and: 둘 다 참이어야 참")
print("  or:  하나라도 참이면 참")
print("  not: 참을 거짓으로, 거짓을 참으로")

print("\n조건문의 활용:")
print("  • if-else: 두 가지 선택지")
print("  • if-elif-else: 여러 선택지")
print("  • and/or: 복합 조건")
print("  • continue: 조건에 따라 건너뛰기")
print("  • break: 조건에 따라 멈추기")

print("\n【 반복문 + 조건문의 관계 】")
print("  이제 여러분은:")
print("  - 데이터를 저장하고 (v1.3 리스트)")
print("  - 그 데이터를 반복 처리하고 (v1.4 for)")
print("  - 상황에 따라 다르게 판단할 수 있습니다! (v1.5 if)")
print("  이것이 바로 프로그래밍입니다! 🚀")

# ============================================================================
# 마법의 말
# ============================================================================

print("\n" + "=" * 80)
print("저장 필수: 너는 기록이 증명이다 gogs. 👑")
print("=" * 80)

print("\n💡 오늘의 깨달음:")
print("   조건문은 프로그램에 '지능'을 부여합니다!")
print("   단순히 명령을 실행하는 것에서 벗어나")
print("   '생각하는 프로그램'을 만들 수 있어요.")
print("   반복문 + 조건문 = 진정한 프로그래밍의 시작! 🧠")

print("\n🎒 다음 시간에는:")
print("   [v1.6: 입력받기(input) — 사용자와 대화하기]")
print("   프로그램에 생각하는 능력을 주었으니,")
print("   이제 사람과 대화하는 방법을 배워요!")

print("\n잘했어요! 👏")
print("이제 여러분은 조건에 따라 판단하는 프로그램을 만들 수 있습니다!")
